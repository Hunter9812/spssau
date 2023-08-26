<template>
    <el-upload
        loading
        ref="upload"
        class="upload-demo"
        :action="actionUrl"
        accept=".xlsx, .xls, .csv"
        :show-file-list="false"
        :limit="1"
        :before-upload="beforeUpload"
        :on-success="handleSuccess"
        :on-error="handleError"
    >
        <el-button type="primary" plain>上传文件</el-button>
        <template #tip>
            <div class="el-upload__tip text-red">
                限制单个文件，新文件将覆盖旧文件
            </div>
        </template>
    </el-upload>
</template>

<script setup lang="ts">
import type { UploadInstance } from "element-plus";
import { ElMessage } from "element-plus";
import { ref } from "vue";
import request from '../utils/request';
const actionUrl = request.defaults.baseURL + '/api/upload/'
const upload = ref<UploadInstance>();
const emit = defineEmits<{
    "upload-data": [fileInfo: any];
}>();

const beforeUpload = (file: File) => {
    const limitMB = 20;
    const fileType = file.name.split(".").pop()!.toLowerCase();
    const allowedTypes = ["xlsx", "xls", "csv"];
    const isAllowedType = allowedTypes.includes(fileType);
    const isLtMB = file.size / 1024 / 1024 <= limitMB;

    if (!isAllowedType) {
        ElMessage.error("只能上传 .xlsx, .xls, .csv 格式的文件");
    }
    if (!isLtMB) {
        ElMessage.error(`文件大小不能超过 ${limitMB}MB`);
    }
    return isAllowedType && limitMB;
};

const handleSuccess = (response: any) => {
    upload.value!.clearFiles();
    const code = response.ret;
    if (code == 1) {
        ElMessage.success("上传成功");
        let data = {
            headers: response.headers,
            name: response.name,
        };
        emit("upload-data", data);
    } else if (code == 0) ElMessage.error(response.msg);
    else ElMessage.error("未知错误");
};

const handleError = (err: Error) => {
    ElMessage.error("上传失败");
    console.error(err);
};
</script>
