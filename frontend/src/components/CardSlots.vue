<template>
    <el-card class="box-card">
        <slot name="header"></slot>
        <el-divider border-style="double" />
        <el-scrollbar height="60vh">
            <slot name="content"></slot>
        </el-scrollbar>
    </el-card>
</template>
<style scoped>
.box-card {
    height: 80vh;
}
</style>
