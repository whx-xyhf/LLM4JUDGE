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
                        @click="openUploadBox">OPEN</el-button>
                    <el-button icon="el-icon-download"
                        style="height:47px;background:#f5f5f5;color:#000;border:none;transition: opacity .2s cubic-bezier(0.4, 0, 0.6, 1);"
                        @click="handleDownload">SAVE</el-button>
                    <input type="file" name="" id="fileInput" @change="uploadFile($event)" style="display:none">
                </div>
            </div>
        </el-header>
        <el-container>
            <!-- <el-aside width="300px" style="height:calc(100vh - 48px);padding:5px 5px">
                
                
            </el-aside> -->
            <!-- #f0f2f5; -->
            <el-main
                style="height:calc(100vh - 48px); position:relative; width: calc(100% - 0px);padding:10px;box-sizing:border-box;background: white"
                class="main">
                <div class="filter-container" style="display:flex; padding:0 0 5px 0;">
                    <el-input v-model="listQuery.phenomenon" placeholder="故障名称" style="width: 200px;margin-right:5px" class="filter-item" @keyup.enter.native="handleFilter" />
                    <el-select v-model="listQuery.status" placeholder="状态" clearable class="filter-item" style="width: 130px;margin-right:5px">
                        <el-option v-for="item in allStatus" :key="item.key" :label="item" :value="item" />
                    </el-select>
                    <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter" style="margin-right:5px;margin-left: 5px;">
                        筛选
                    </el-button>
                    <el-button class="filter-item" style="margin-right: 5px;margin-left: 5px;" type="primary" icon="el-icon-edit" @click="handleCreate">
                        手动增加行
                    </el-button>
                    <el-input v-model="listQuery.limit" placeholder="请输入单次获取条数" style="width: 200px;margin-right:5px"/>
                    <el-button class="filter-item" style="margin-right: 5px;margin-left: 5px;" type="primary" icon="el-icon-edit" @click="getTotalList">
                        启动梳理
                    </el-button>
                </div>

                <el-table
                    :key="tableKey"
                    v-loading="listLoading"
                    :data="list"
                    border
                    fit
                    highlight-current-row
                    style="width: 100%;"
                    >
                    <el-table-column label="序号" prop="id" align="center" width="80">
                        <template slot-scope="{row}">
                        <span>{{ row.id }}</span>
                        </template>
                    </el-table-column>
                    
                    <el-table-column label="故障名称" width="120px" align="center">
                        <template slot-scope="{row}">
                        <span>{{ row.phenomenon }}</span>
                        </template>
                    </el-table-column>

                    <el-table-column label="判据" align="center" min-width="150px">
                        <template slot-scope="{row}">
                        <span>{{ row.condition }}</span>
                        </template>
                    </el-table-column>

                    <el-table-column label="规程" min-width="150px" align="center">
                        <template slot-scope="{row}">
                        <span>{{ row.rule }}</span>
                        </template>
                    </el-table-column>

                    <el-table-column label="运行参数" min-width="150px" align="center">
                        <template slot-scope="{row}">
                        <span>{{ row.parameter }}</span>
                        </template>
                    </el-table-column>

                    <el-table-column v-for="i in exampleCount" :key="'example'+i" :label="'案例'+i" min-width="150px" align="center">
                        <template slot-scope="{row}">
                        <span>{{ row['example'+i] }}</span>
                        </template>
                    </el-table-column>

                    <el-table-column label="状态" class-name="status-col" width="80">
                        <template slot-scope="{row}">
                        <el-tag :type="row.status | statusFilter">
                            {{ row.status }}
                        </el-tag>
                        </template>
                    </el-table-column>

                    <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
                        <template slot-scope="{row,$index}">
                        <el-button type="primary" size="mini" @click="handleUpdate(row)">
                            编辑
                        </el-button>
                        <el-button v-if="row.status!='已校准'" size="mini" type="success" @click="handleModifyStatus(row,'已校准')">
                            校准
                        </el-button>
                        <el-button v-if="row.status!='未校准'" size="mini" @click="handleModifyStatus(row,'未校准')">
                            打回
                        </el-button>
                        <el-button v-if="row.status!='删除'" size="mini" type="danger" @click="handleDelete(row,$index)">
                            删除
                        </el-button>
                        </template>
                    </el-table-column>

                </el-table>

                <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

            </el-main>
        </el-container>

        <el-dialog title="File Upload" :visible.sync="dialogFormVisible">
            <el-form ref="fileForm" label-position="left" label-width="100px" style="width: 400px; margin-left:50px;">
                <el-form-item label="规程文件：">
                    <div class="upload-panel-type">
                        <el-upload
                            class="upload-demo"
                            ref="uploadGuicheng"
                            :action="uploadUrl.guicheng"
                            :on-preview="handlePreview"
                            :on-remove="handleRemove"
                            :file-list="guichengList"
                            :on-success="handleSuccessGuicheng"
                            :auto-upload="false"
                            multiple>
                            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
                            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload('Guicheng')">上传到服务器</el-button>
                            <div slot="tip" class="el-upload__tip">只能上传json文件</div>
                        </el-upload>
                    </div>
                </el-form-item>

                <el-form-item label="运行参数：">
                    <div class="upload-panel-type">
                        <el-upload
                            class="upload-demo"
                            ref="uploadValue"
                            :action="uploadUrl.dingzhiqingce"
                            :on-preview="handlePreview"
                            :on-remove="handleRemove"
                            :file-list="valueList"
                            :auto-upload="false"
                            multiple>
                            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
                            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload('Value')">上传到服务器</el-button>
                            <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
                        </el-upload>
                    </div>
                </el-form-item>

                <el-form-item label="判据案例：">
                    <div class="upload-panel-type">
                        <el-upload
                            class="upload-demo"
                            ref="uploadExample"
                            :action="uploadUrl.example"
                            :on-preview="handlePreview"
                            :on-remove="handleRemove"
                            :on-success="handleSuccessExample"
                            :file-list="exampleList"
                            :auto-upload="false"
                            multiple>
                            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
                            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload('Example')">上传到服务器</el-button>
                            <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
                        </el-upload>
                    </div>
                </el-form-item>
              
            </el-form>

        </el-dialog>

        <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisibleUpdate">
        <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="100px" style="width: 400px; margin-left:50px;">
            <el-form-item label="故障名称：" prop="phenomenon">
            <el-input v-model="temp.phenomenon" @input="changeMessage()" />
            </el-form-item>

            

            <el-form-item label="判据：" prop="condition">
            <el-input v-model="temp.condition" @input="changeMessage()" />
            </el-form-item>

            <el-form-item label="规程：" prop="rule">
            <el-input v-model="temp.rule" @input="changeMessage()" />
            </el-form-item>

            <el-form-item label="运行参数：">
            <el-input v-model="temp.parameter" @input="changeMessage()" />
            </el-form-item>

            <el-form-item v-for="i in exampleCount" :label="'exam'+i+'：'" :key="'案例'+i" prop="rule">
            <el-input v-model="temp['example'+i]" @input="changeMessage()" />
            </el-form-item>

            <el-form-item label="状态：" prop="rule">
            <el-select v-model="temp.status" class="filter-item" placeholder="Please select" style="float:left" @change="changeMessage()" >
                <el-option v-for="item in allStatus" :key="item" :label="item" :value="item" />
            </el-select>
            </el-form-item>
            
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisibleUpdate = false">
            Cancel
            </el-button>
            <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
            Confirm
            </el-button>
        </div>
    </el-dialog>

    </el-container>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
export default {
    name: 'Layout',
    components: { Pagination },
    directives: { waves },
    filters: {
        statusFilter(status) {
            const statusMap = {
                '已校准': 'success',
                '未校准': 'info',
                '删除': 'danger'
            }
            return statusMap[status]
        },
    },
    data() {
        return {
            uploadUrl:{guicheng:'/api/uploadGuicheng', dingzhiqingce:'/api/uploadValue', example:'/api/uploadExample'},
            socket: null,
            tableKey: 0,
            fileTemp:[],
            temp:[],
            listLoading: false,
            allStatus:['未校准', '已校准'],
            statusOptions: ['未校准', '已校准', '删除'],
            dialogFormVisible: false,//show 上传文件
            dialogFormVisibleUpdate:false,//show 更新表格
            exampleCount:0,
            list: [],
            totalList: [],
            dialogStatus: '',
            textMap: {
                update: 'Edit',
                create: 'Create'
            },
            exportExcelName:'判据',
            total:0,
            rules: {
                phenomenon: [{ required: true, message: '现象不能为空！', trigger: 'change' }],
                condition: [{ required: true, message: '判据不能为空！', trigger: 'change' }],
                status: [{ required: true, message: '状态不能为空！', trigger: 'change' }],
            },
            listQuery: {
                page: 1,
                limit: 5,
                phenomenon:'',
                status:'',
            },
            exampleList: [],
            valueList: [],
            guichengList:[],
        }
    },
    methods: {
        openUploadBox(){
            this.dialogFormVisible = true;
        },
        clickFile() {
            document.getElementById("fileInput").click();
        },
        submitUpload(type) {
            this.$refs['upload'+type].submit();
            console.log(this.exampleList)
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        },
        handleSuccessExample(res, file, fileList){
            this.exampleCount = fileList.length;
            this.resetTemp()
        },
        handleSuccessGuicheng(res, file, fileList){
            this.guichengList = fileList
        },
        // uploadFile(e) {
        //     const fileName = e.target.files[0].name.split('.')[0];
        //     this.fileName = fileName;

        //     if (window.FileReader) {
        //         //创建读取文件的对象
        //         var fr = new FileReader();
        //         //以读取文件字符串的方式读取文件 但是不能直接读取file 
        //         //因为文件的内容是存在file对象下面的files数组中的
        //         //该方法结束后图片会以data:URL格式的字符串（base64编码）存储在fr对象的result中
        //         fr.readAsDataURL(e.target.files[0]);
        //         fr.onloadend = () => {

        //         }
        //     }
        // },
        getList(){
            if(this.listQuery.phenomenon == '' && this.listQuery.status == ''){
                this.total = this.totalList.length;
                this.list = this.totalList.slice((this.listQuery.page-1) * this.listQuery.limit, this.listQuery.page * this.listQuery.limit)
            }
            else{
                let list = this.totalList.filter(item=>{
                    let flag1 = true;
                    let flag2 = true;
                    if(this.listQuery.phenomenon != ''){
                        if(item.phenomenon.indexOf(this.listQuery.phenomenon)>=0){
                            flag1 = true;
                        }
                        else{
                            flag1 = false;
                        }
                    }
                    if(this.listQuery.status != ''){
                        console.log(item.status, this.listQuery.status)
                        if(item.status == this.listQuery.status){
                            flag2 = true;
                        }
                        else{
                            flag2 = false;
                        }
                    }
                    return flag1 && flag2
                })
                this.total = list.length;
                this.list = list.slice((this.listQuery.page-1) * this.listQuery.limit, this.listQuery.page * this.listQuery.limit)
            }
            
        },
        getTotalList() {
            if(this.guichengList.length == 0){
                alert("请首先上传规程文件！")
                return;
            }
            this.$axios.post('./getResult',{limit: this.listQuery.limit, total:this.total}).then(response=>{
                if(response.data.code == 200){
                    console.log(response.data.status)
                    if(response.data.status){
                        alert("规程已经梳理完！")
                    }
                    else{
                        this.totalList = this.totalList.concat(response.data.data);
                        this.getList();
                    }
                }
                else{
                    alert("Error")
                }
            })
            // this.listLoading = true
            // fetchList(this.listQuery).then(response => {
            //     this.list = response.data.items
            //     this.total = response.data.total

            //     // Just to simulate the time of the request
            //     setTimeout(() => {
            //     this.listLoading = false
            //     }, 1.5 * 1000)
            // })
        },
        handleFilter() {
            this.listQuery.page = 1
            this.getList()
        },
        resetTemp() {
            this.temp = {
                id: undefined,
                condition: '',
                phenomenon: '',
                rule: '',
                parameter:'',
                status: '未校准'
            }
            for(let i = 0 ; i < this.exampleCount; i++){
                let index = i + 1;
                this.temp['example'+index] = ''
            }
        },
        handleModifyStatus(row, status) {
            this.$message({
                message: '操作Success',
                type: 'success'
            })
            row.status = status
        },
        handleCreate() {
            this.resetTemp()
            this.dialogStatus = 'create'
            this.dialogFormVisibleUpdate = true
            this.$nextTick(() => {
                this.$refs['dataForm'].clearValidate()
            })
        },
        createData() {
            this.$refs['dataForm'].validate((valid) => {
                this.temp.id = this.totalList.length + 1;
                if (valid) {
                    this.list.unshift(this.temp)
                    this.totalList.unshift(this.temp)
                    this.dialogFormVisibleUpdate = false
                    this.$notify({
                        title: 'Success',
                        message: 'Created Successfully',
                        type: 'success',
                        duration: 2000
                    })
                }
            })
        },
        handleUpdate(row) {
            this.temp = Object.assign({}, row) // copy obj
            this.dialogStatus = 'update'
            this.dialogFormVisibleUpdate = true
            this.$nextTick(() => {
                this.$refs['dataForm'].clearValidate()
            })
        },
        updateData() {
        this.$refs['dataForm'].validate((valid) => {
            if (valid) {
                const index_ = this.totalList.findIndex(v => v.id === this.temp.id)
                const index = this.list.findIndex(v => v.id === this.temp.id)
                this.list.splice(index, 1, this.temp)
                this.totalList.splice(index_, 1, this.temp)
                this.$notify({
                    title: 'Success',
                    message: 'Update Successfully',
                    type: 'success',
                    duration: 2000
                })
                this.dialogFormVisibleUpdate = false;
                }
            })
        },
        handleDelete(row, index) {
            const index_ = this.totalList.findIndex(v => v.id === this.temp.id)
            this.list.splice(index, 1)
            this.totalList.splice(index_, 1, this.temp)
            this.$notify({
                title: 'Success',
                message: 'Delete Successfully',
                type: 'success',
                duration: 2000
            })
        },
        changeMessage: function () {// 强制更新测试文本信息框的值
            this.$forceUpdate();
        },
        // 导出excel
        handleDownload() {
            if (this.totalList.length > 0) {
                import('@/vendor/Export2Excel').then(excel => {
                    const tHeader = ['序号', '故障名称', '判据', '规程', '定值清测'];
                    
                    const filterVal = ['id', 'phenomenon', 'condition', 'rule', 'parameter'];
                    for(let i=0; i< this.exampleCount; i++){
                        tHeader.push('案例'+i);
                        filterVal.push('example'+i);
                    }
                    tHeader.push('状态');
                    filterVal.push('status');
                    const data = this.formatJson(filterVal)
                    excel.export_json_to_excel({
                        header: tHeader,
                        data,
                        filename: this.exportExcelName
                    })
                })
            }
            else {
                alert('The data is Empty');
            }
        },
        formatJson(filterVal) {
            return this.totalList.map(v => filterVal.map(j => {
                return v[j]
            }))
        },
    },

    mounted(){
        // this.getTotalList();
        
    },
    watch: {

    }
}
</script>
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