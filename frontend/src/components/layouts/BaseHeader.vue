<template>
    <el-menu
        class="el-menu-demo"
        mode="horizontal"
        :router="true"
        :default-active="'analysis'"
        :ellipsis="true"
    >
        <el-menu-item index="" id="logo">小目标</el-menu-item>
        <el-menu-item index="analysis">数据分析</el-menu-item>

        <div class="flex-grow"></div>

        <el-menu-item index="about">About</el-menu-item>
    </el-menu>
</template>
