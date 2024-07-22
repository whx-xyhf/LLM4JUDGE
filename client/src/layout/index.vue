<template>
    <el-container>
        <el-header height="48px" style="box-shadow: 0px 2px 4px -1px rgb(0 0 0 20%), 0px 4px 5px 0px rgb(0 0 0 / 14%), 0px 1px 10px 0px rgb(0 0 0 / 12%);
    background-color: #f5f5f5;padding: 0">
            <div class="tool_bar_content">
                <div style="font-weight:700">
                    基于规程文件和样例判据数据的判据梳理系统
                </div>
                <div class="spacer"></div>
                <div class="tool_bar__items">
                    <el-button icon="el-icon-folder"
                        style="height:47px;background:#f5f5f5;color:#000;border:none;transition: opacity .2s cubic-bezier(0.4, 0, 0.6, 1);"
                        ><router-link to="/guichen">规程梳理</router-link></el-button>
                    <el-button icon="el-icon-folder"
                        style="height:47px;background:#f5f5f5;color:#000;border:none;transition: opacity .2s cubic-bezier(0.4, 0, 0.6, 1);"
                        ><router-link to="/anli">案例梳理</router-link></el-button>
                </div>
            </div>
        </el-header>
        <el-main
                style="height:calc(100vh - 48px); position:relative; width: calc(100% - 0px);padding:10px;box-sizing:border-box;background: white"
                class="main">
            <router-view></router-view>
        </el-main>
    </el-container>
</template>

<style scoped>
.tool_bar_content {
    height: 48px;
    padding: 0px 16px;
    display: flex;
    position: relative;
    align-items: center;
    font-size: 0.9rem;
    box-sizing: border-box;
    border-bottom: 1px solid #d8dce5;
}

.tool_bar__items button:hover {
    background-color: #ccc;
}

.tool_bar_btn__content {
    align-items: center;
    color: inherit;
    display: flex;
    flex: 1 0 auto;
    justify-content: inherit;
    line-height: normal;
    position: relative;
    transition: inherit;
    transition-property: opacity;
}

.spacer {
    flex-grow: 1 !important;
}

.tool_bar__items {
    display: flex;
    height: inherit;
}

.filter-container {
    padding-bottom: 10px;
}
</style>

<style>
.el-slider__button {
    border-radius: 30% !important;
}
</style>