<template>
    <el-container>
        <el-main>
            <el-row :gutter="5">
                <el-col :span="4">
                    <card-slots>
                        <template #header>
                            <h1>{{ ruleForm.name }}</h1>
                            <up-load-button
                                @upload-data="showFileInfo($event)"
                            ></up-load-button>
                        </template>
                        <template #content>
                            <file-head-info
                                :fileHeadInfoArray="fileHeadInfoArray"
                            ></file-head-info>
                        </template>
                    </card-slots>
                </el-col>
                <el-col :span="4">
                    <card-slots>
                        <template #header>
                            <h1>选择算法</h1>
                        </template>
                        <template #content>
                            <el-collapse v-model="activeCollapseName" accordion>
                                <el-collapse-item title="方差分析" name="1">
                                    <div
                                        class="item"
                                        v-for="(value, key) in list"
                                        :key="key"
                                        @click="selectArithmetic(key)"
                                    >
                                        {{ value }}
                                    </div>
                                </el-collapse-item>
                            </el-collapse>
                        </template>
                    </card-slots>
                </el-col>
                <el-col :span="4">
                    <card-slots>
                        <template #header>
                            <h1>选择变量</h1>
                        </template>
                        <template #content>
                            <el-empty
                                v-if="
                                    ruleForm.anovaType === '' ||
                                    ruleForm.name === ''
                                "
                                :image-size="100"
                            />
                            <div v-else>
                                <el-form
                                    label-position="top"
                                    ref="ruleFormRef"
                                    status-icon
                                    :model="ruleForm"
                                    :rules="rules"
                                >
                                    <el-form-item label="自变量：" prop="xid">
                                        <el-input
                                            v-model="ruleForm.xid"
                                            placeholder="请输入ID"
                                        />
                                    </el-form-item>
                                    <el-form-item label="因变量：" prop="yid">
                                        <el-input
                                            v-model="ruleForm.yid"
                                            placeholder="请输入ID"
                                        />
                                    </el-form-item>
                                    <el-text class="mx-1" type="danger"
                                        >用,(英文逗号)分隔</el-text
                                    >
                                    <el-form-item>
                                        <el-button
                                            type="primary"
                                            @click="submitForm(ruleFormRef)"
                                            >提交</el-button
                                        >
                                        <el-button
                                            @click="resetForm(ruleFormRef)"
                                            >重置</el-button
                                        >
                                    </el-form-item>
                                </el-form>
                            </div>
                        </template>
                    </card-slots>
                </el-col>

                <el-col :span="12">
                    <card-slots>
                        <template #header>
                            <h1>方差分析</h1>
                        </template>
                        <template #content>
                            <el-empty v-if="!resultAnalyse.value" />
                            <analyse-info
                                v-else
                                :resultAnalyse="resultAnalyse.value"
                            ></analyse-info>
                        </template>
                    </card-slots>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { reactive, ref } from "vue";
import CardSlots from "../components/CardSlots.vue";
import FileHeadInfo from "../components/FileHeadInfo.vue";
import UpLoadButton from "../components/UpLoadButton.vue";
import analyseInfo from "../components/analyseInfo.vue";
import request from "../utils/request";

const activeCollapseName = ref("1");
const list = { 1: "单因素方差分析", 2: "两因素方差分析", 3: "多因素方差分析" };
const fileHeadInfoArray = ref([]);
const ruleFormRef = ref({});
const ruleForm = reactive({
    name: "",
    xid: "",
    yid: "",
    anovaType: "",
});
const resultAnalyse = reactive({});

const validatePass = (rule, value, callback) => {
    if (value === "") {
        callback(new Error("输入为空"));
    } else {
        if (ruleForm.xid !== "") {
            if (!ruleFormRef.value) return;
            ruleFormRef.value.validateField("yid", () => null);
        }
        callback();
    }
};

const validatePass2 = (rule, value, callback) => {
    if (value === "") {
        callback(new Error("输入为空"));
    } else {
        callback();
    }
};

const rules = reactive({
    xid: [{ validator: validatePass, trigger: "blur" }],
    yid: [{ validator: validatePass2, trigger: "blur" }],
});

const submitForm = (formEl) => {
    if (!formEl) return;
    formEl.validate((valid) => {
        if (valid) {
            const plainData = ruleForm;
            const formData = new FormData();
            for (const key in plainData) {
                if (plainData.hasOwnProperty(key)) {
                    formData.append(key, plainData[key]);
                }
            }
            request
                .post("/api/app01/variance_analysis", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .then((response) => {
                    // 处理请求成功的逻辑
                    response = response.data;
                    const code = response.ret;
                    if (code == 1) {
                        ElMessage.success("分析成功");
                        resultAnalyse.value = response.result;
                    } else if (code == 0) ElMessage.error(response.msg);
                    else ElMessage.error("未知错误");
                })
                .catch((error) => {
                    // 处理请求失败的逻辑
                    console.error(error);
                    ElMessage.error("分析失败");
                });
        } else {
            ElMessage.error("数据错误");
            return false;
        }
    });
};

const resetForm = (formEl) => {
    if (!formEl) return;
    formEl.resetFields();
};

const selectArithmetic = (item) => {
    ruleForm.anovaType = item;
};

const showFileInfo = (data) => {
    ruleForm.xid = "";
    ruleForm.yid = "";
    ruleForm.anovaType = "";
    resultAnalyse.value = "";
    ruleForm.name = data.name;
    const newArray = Object.entries(data.headers).map(([id, name]) => {
        return {
            id: parseInt(id),
            name,
        };
    });
    fileHeadInfoArray.value = newArray;
};
</script>

<style scoped>
.item {
    text-align: left; /* 左对齐 */
    padding: 10px 5px;
}
.item:hover {
    background-color: #f9f9f9; /* 设置悬停时的背景颜色 */
    cursor: pointer;
}
</style>
