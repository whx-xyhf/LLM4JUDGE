<template>
    <el-container>
        <el-header height="64px" style="box-shadow: 0px 2px 4px -1px rgb(0 0 0 20%), 0px 4px 5px 0px rgb(0 0 0 / 14%), 0px 1px 10px 0px rgb(0 0 0 / 12%);
    background-color: #f5f5f5;padding: 0">
            
        </el-header>
        <el-container>
            <el-aside width="300px" style="height:calc(100vh - 64px);padding:5px 5px">

            </el-aside>
            <el-main
                style="height:calc(100vh - 64px); position:relative; width: calc(100% - 300px);padding:0;box-sizing:border-box;background: #ddd;"
                class="main">
                
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
    name: 'Layout',
    data() {
        return {
            
        }
    },
    methods: {
        clickFile() {
            document.getElementById("fileInput").click();
        },
        test(){
            this.$axios.post("/test", {"message":"hello"}).then(res=>{
                if(res.data.code == 200){
                    alert(res.data.data);
                }
            })
        },
        uploadFile(e) {
            const fileName = e.target.files[0].name.split('.')[0];
            this.fileName = fileName;

            if (window.FileReader) {
                //创建读取文件的对象
                var fr = new FileReader();
                //以读取文件字符串的方式读取文件 但是不能直接读取file 
                //因为文件的内容是存在file对象下面的files数组中的
                //该方法结束后图片会以data:URL格式的字符串（base64编码）存储在fr对象的result中
                fr.readAsDataURL(e.target.files[0]);
                fr.onloadend = () => {

                }
            }
        },

        //导出excel
        // handleDownload() {
        //     if (this.tableData.length > 0) {
        //         import('@/vendor/Export2Excel').then(excel => {
        //             const tHeader = ['Length', 'RealDiameter', 'Diameter'];
        //             const filterVal = ['Length', 'RealDiameter', 'Diameter'];
        //             const data = this.formatJson(filterVal)
        //             excel.export_json_to_excel({
        //                 header: tHeader,
        //                 data,
        //                 filename: this.fileName + '_Radius'
        //             })
        //         })
        //     }
        //     else {
        //         alert('The data is Empty');
        //     }
        // },
        // formatJson(filterVal) {
        //     return this.tableData.map(v => filterVal.map(j => {
        //         return v[j]
        //     }))
        // },
    },
    mounted(){
        this.test();
    },
    watch: {

    }
}
</script>
<style scoped>

</style>
<style>
.el-slider__button {
    border-radius: 30% !important;
}
</style>