from django.http import JsonResponse
from django.conf import settings
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import os
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import numpy as np


@csrf_exempt
def analyze_selected_columns(request):
    if request.method == "POST":
        file_name = request.POST.get("name")
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        selected_column = request.POST.get("xid")
        xcolumns = [int(x) for x in selected_column.split(",")]
        selected_column = request.POST.get("yid")
        ycolumns = [int(x) for x in selected_column.split(",")]

        anova_method = request.POST.get("anovaType")

        if os.path.exists(file_path):
            file_type = os.path.splitext(file_path)[1].lower()

            if file_type in [".xls", ".xlsx"]:
                # 使用 pandas 读取 Excel 文件
                df = pd.read_excel(file_path)
            elif file_type == ".csv":
                df = pd.read_csv(file_path)
            else:
                return JsonResponse({"ret": "0", "msg": "不支持该文件类型"})

            try:
                # 检查是否存在选中的列名
                columns = list(range(len(df.columns)))
                columns_exist = all(
                    col_name in columns for col_name in xcolumns
                ) and all(col_name in columns for col_name in ycolumns)
                if not columns_exist:
                    return JsonResponse({"ret": "0", "msg": "指定的列名不存在"})

                # 根据选中的列名提取数据子集
                x_df = df.iloc[:, xcolumns]
                y_df = df.iloc[:, ycolumns]
                # 执行方差分析
                if anova_method == "1":
                    result = single_factor_analysis(xcolumns, ycolumns, df)
                elif anova_method == "2":
                    result = two_factor_analysis(xcolumns, ycolumns, df)
                else:
                    result = multi_factor_analysis(xcolumns, ycolumns, df)

                return JsonResponse({"ret": "1", "result": result})

            except Exception as e:
                return JsonResponse({"ret": "0", "msg": str(e)})
        else:
            return JsonResponse({"ret": "0", "msg": "未收到文件"})
    else:
        return JsonResponse({"ret": "0", "msg": "仅支持 POST 请求"})


def single_factor_analysis(xid, yid, df):
    # 确定自变量和因变量的列名
    # 自变量
    independent_var = df.columns[xid]
    # 因变量
    dependent_var = df.columns[yid]
    # 执行单因素方差分析
    data = {}
    backmsg = ""
    headmsg = "从上表可知，利用方差分析(全称为单因素方差分析)去研究组别对于{}共{}项的差异性,".format(
        ",".join(dependent_var.tolist()), len(dependent_var)
    )
    for depe in dependent_var:
        formula = f"{depe} ~ {independent_var[0]}"
        model = ols(formula, data=df).fit()
        anova_result = anova_lm(model).fillna('NaN')
        data[depe] = anova_result.to_dict()
        if anova_result.iloc[0, 4] > 0.05:
            backmsg += "从上表可以看出：不同{}样本对于{}全部均不会表现出显著性(<i>p</i>>0.05)，意味着不同{}样本对于{}全部均表现出一致性，并没有差异性</br>".format(
                independent_var[0], depe, independent_var[0], depe
            )
        else:
            backmsg += "从上表可以看出：不同{}样本对于{}均呈现出显著性(<i>p</i><0.05)，意味着不同{}样本对于{}全部均有着显著性，均有着差异性.</br>".format(
                independent_var[0], depe, independent_var[0], depe
            )
    result = {
        "data": data,
        "analyse": "方差分析研究X(定类)对于Y(定量)的差异，比如不同学历人群对满意度差异关系；</br>第一：分析X与Y之间是否呈现出显著性(<i>p</i>值小于0.05或0.01)；</br>第二：如果呈现出显著性；通过具体对比平均值大小，描述具体差异所在；</br>第三：如果没有呈现出显著性；说明X不同组别下，Y没有差异；</br>第四：对分析进行总结。",
        "autoAnalyse": headmsg + backmsg,
    }
    # 返回结果
    return result


def two_factor_analysis(xid, yid, df):
    # 自变量
    independent_var = df.columns[xid]
    # 因变量
    dependent_var = df.columns[yid]
    # 执行单因素方差分析
    data = {}
    backmsg = ""
    headmsg = "从上表可知，利用双因素方差分析去研究{}和{}对于{}的影响关系，从上表可以看出：".format(
        independent_var[0], independent_var[1], dependent_var[0]
    )
    formula = f"{dependent_var[0]} ~ {independent_var[0]} + {independent_var[1]}"
    model = ols(formula, data=df).fit()
    anova_result = anova_lm(model).fillna('NaN')
    data[dependent_var[0]] = anova_result.to_dict()
    for i in range(0, 2):
        if anova_result.iloc[i, 4] < 0.05:
            backmsg += "{}呈现出显著性(<i>F</i>={}，<i>p</i>={}<0.05) ，说明主效应存在，{}会对{}产生差异关系。具体差异可通过方差分析(单因素)进行具体分析。</br>".format(
                independent_var[i],
                anova_result.iloc[i, 3],
                anova_result.iloc[i, 4],
                independent_var[i],
                dependent_var[0],
            )
        else:
            backmsg += "{}没有呈现出显著性(<i>F</i>={}，<i>p</i>={}>0.05) ，说明主效应不存在，{}不会对{}产生差异关系。</br>".format(
                independent_var[i],
                anova_result.iloc[i, 3],
                anova_result.iloc[i, 4],
                independent_var[i],
                dependent_var[0],
            )

    result = {
        "data": data,
        "analyse": "双因素方差分析用于研究2个定类数据X对于1个定量数据Y的差异关系，通常用于实验研究中。如果有可能干扰模型项，则放入协变量中。</br>第一：分别分析2个X是否呈现出显著性；如果呈现出显著性，说明X不同组别会对Y产生显著性差异，具体可以通过方差分析(单因素方差)进一步研究；</br>第二：如果二阶效应显著(且前提是存在一阶主效应)，可继续通过表格和图形研究二阶效应情况【二阶效应也称作交互效应,需要选中才会输出】；</br>第三：协变量为干扰项，通常不需要进行分析。",
        "autoAnalyse": headmsg + backmsg,
    }
    # 返回结果
    return result


def multi_factor_analysis(xid, yid, df):
    # 自变量
    independent_var = df.columns[xid]
    # 因变量
    dependent_var = df.columns[yid]
    # 执行单因素方差分析
    data = {}
    backmsg = ""
    headmsg = "从上表可知，利用多因素方差分析去研究{}对于{}的影响关系，从上表可以看出：".format(
        ",".join(independent_var.tolist()), dependent_var[0]
    )
    formula = f'{dependent_var[0]} ~ {" + ".join(independent_var)}'
    model = ols(formula, data=df).fit()
    anova_result = anova_lm(model).fillna('NaN')
    data[dependent_var[0]] = anova_result.to_dict()
    for i in range(0, len(independent_var)):
        if anova_result.iloc[i, 4] < 0.05:
            backmsg += "{}呈现出显著性(<i>F</i>={}，<i>p</i>={}<0.05) ，说明主效应存在，{}会对{}产生差异关系。具体差异可通过方差分析(单因素)进行具体分析。</br>".format(
                independent_var[i],
                anova_result.iloc[i, 3],
                anova_result.iloc[i, 4],
                independent_var[i],
                dependent_var[0],
            )
        else:
            backmsg += "{}没有呈现出显著性(<i>F</i>={}，<i>p</i>={}>0.05) ，说明{}并不会对{}产生差异关系。</br>".format(
                independent_var[i],
                anova_result.iloc[i, 3],
                anova_result.iloc[i, 4],
                independent_var[i],
                dependent_var[0],
            )

    result = {
        "data": data,
        "analyse": "多因素方差分析用于研究多个定类数据X对于1个定量数据Y的差异关系，通常用于实验研究中。如果有可能干扰模型项，则放入协变量中。</br>第一：分别分析多个X是否呈现出显著性；如果呈现出显著性，说明X不同组别会对Y产生显著性差异，具体可以通过方差分析(单因素方差)进一步研究；</br>第二：如果二阶效应显著(且前提是存在一阶主效应)，可继续通过表格和图形研究二阶效应情况；</br>第三：如果三阶效应显著(且前提是存在二阶效应)；可继续通过表格均值对比研究三阶效应情况；</br>第四：协变量为干扰项，通常不需要进行分析。",
        "autoAnalyse": headmsg + backmsg,
    }
    # 返回结果
    return result
