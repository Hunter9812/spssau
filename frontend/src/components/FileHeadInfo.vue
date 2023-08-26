<template>
    <div>
        <el-scrollbar height="60vh">
            <el-table :data="fileHeadInfoArray">
                <el-table-column prop="id" label="ID" width="60vw"/>
                <el-table-column prop="name" label="名字" />
            </el-table>
        </el-scrollbar>
    </div>
</template>

<script setup>
const props = defineProps({
    fileHeadInfoArray: { type: Array, required: false }
});
</script>
