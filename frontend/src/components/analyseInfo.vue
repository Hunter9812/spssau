<template>
    <h2>分析结果</h2>
    <div v-html="resultAnalyse.analyse"></div>
    <h2>详细结论</h2>
    <div>
        <el-table
            :data="modifiedProp"
            border
            style="width: 100%"
        >
            <el-table-column prop="因变量" label="因变量" />
            <el-table-column prop="自变量" label="自变量/参数" />
            <el-table-column prop="df" label="df" />
            <el-table-column prop="sum_sq" label="sum_sq" />
            <el-table-column prop="mean_sq" label="mean_sq" />
            <el-table-column prop="F" label="F" />
            <el-table-column prop="PR(>F)" label="PR(>F)" />
        </el-table>
    </div>
    <h2>图表说明</h2>
    <div v-html="resultAnalyse.autoAnalyse"></div>
</template>

<script setup>
import { onMounted, ref } from "vue";
const props = defineProps({
    resultAnalyse: {
        analyse: {
            type: String,
        },
        autoAnalyse: {
            type: String,
        },
        data: {
            type: Object,
        },
    },
});
const modifiedProp = ref("");
const ds = (data) => {
    const tableDict = {
        因变量: [],
        自变量: [],
        df: [],
        sum_sq: [],
        mean_sq: [],
        F: [],
        "PR(>F)": [],
    };
    const arrKey1 = Object.keys(data);
    const arrKey2 = Object.keys(data[arrKey1[0]]);
    const arrKey3 = Object.keys(data[arrKey1[0]][arrKey2[0]]);
    const n = arrKey1.length;
    const m = arrKey3.length;

    tableDict.因变量 = Array.from(arrKey1, (item) =>
        Array(m).fill(item)
    ).flat();
    tableDict.自变量 = Array.from({ length: n }, () => arrKey3).flat();

    function extractValues(obj, str) {
        const values = [];
        for (let key in obj) {
            let a = obj[key][str];
            for (let b in a) {
                values.push(a[b]);
            }
        }
        return values;
    }
    tableDict.df = extractValues(data, "df");
    tableDict.sum_sq = extractValues(data, "sum_sq");
    tableDict.mean_sq = extractValues(data, "mean_sq");
    tableDict.F = extractValues(data, "F");
    tableDict["PR(>F)"] = extractValues(data, "PR(>F)");

    const objectArray = [];

    for (let i = 0; i < m * n; i++) {
        let obj = {};

        for (let key in tableDict) {
            obj[key] = tableDict[key][i];
        }
        objectArray.push(obj);
    }
    return objectArray;
};
onMounted(() => {
    modifiedProp.value = ds(props.resultAnalyse.data);
});
</script>
