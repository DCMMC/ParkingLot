<template>
  <div class="fillcontain">
    <div class="filter-container">
      <el-input v-model="listQuery.license_plate" :placeholder="'车牌号'" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.phone_number" :placeholder="'手机号'" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleAdd">
        新增车辆
      </el-button>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        导出
      </el-button>
    </div>
    <div class="table_container">
      <el-table
        :data="tableData"
        :expand-row-keys="expendRow"
        :row-key="row => row.license_plate"
        style="width: 100%"
        @expand-change="expand"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="车牌号" label-width="160px">
                <span>{{ props.row.license_plate }}</span>
              </el-form-item>
              <el-form-item label="手机号" label-width="160px">
                <span>{{ props.row.phone_number }}</span>
              </el-form-item>
              <el-form-item label="持有者姓名" label-width="160px">
                <span>{{ props.row.owner_name }}</span>
              </el-form-item>
              <el-form-item
                v-for="card in props.row.cards"
                :key="card.id"
                :label="card.type_name"
              >
                卡号: {{ card.id }} 余额: {{ card.value }}
              </el-form-item>
              <el-form-item label="备注" label-width="160px">
                <span>{{ props.row.addition_info }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="车牌号"
          prop="license_plate"
        />
        <el-table-column
          label="手机号"
          prop="phone_number"
        />
        <el-table-column
          label="持有人姓名"
          prop="owner_name"
        />
        <el-table-column label="操作" width="260">
          <template slot-scope="scope">
            <el-button
              size="small"
              @click="handleEdit(scope.row)"
            >编辑</el-button>
            <el-button class="filter-item" type="danger" size="small" icon="el-icon-search" @click="handleRemove(scope.row)">
              删除车辆
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="Pagination">
        <el-pagination
          :current-page="currentPage"
          :page-size="20"
          layout="total, prev, pager, next"
          :total="count"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
      <el-dialog title="修改停车辆信息" :visible.sync="dialogFormVisible">
        <el-form :model="selectTable">
          <el-form-item label="车牌号" label-width="400px">
            <el-input
              v-model="selectTable.license_plate"
              auto-complete="off"
              :disable="true"
            />
          </el-form-item>
          <el-form-item label="持有人姓名" label-width="400px">
            <el-input v-model="selectTable.owner_name" auto-complete="off" />
          </el-form-item>
          <el-form-item label="手机号" label-width="400px">
            <el-input v-model="selectTable.phone_number" />
          </el-form-item>
          <el-form-item label="备注信息" label-width="400px">
            <el-input v-model="selectTable.addition_info" />
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="updateVehicle">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="添加车辆" :visible.sync="dialogAddVisible">
        <el-form :model="newTable">
          <el-form-item label="车牌号" label-width="400px">
            <el-input
              v-model="newTable.license_plate"
              auto-complete="off"
              :disable="true"
            />
          </el-form-item>
          <el-form-item label="持有人姓名" label-width="400px">
            <el-input v-model="newTable.owner_name" auto-complete="off" />
          </el-form-item>
          <el-form-item label="手机号" label-width="400px">
            <el-input v-model="newTable.phone_number" />
          </el-form-item>
          <el-form-item label="备注信息" label-width="400px">
            <el-input v-model="newTable.addition_info" />
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogAddVisible = false">取 消</el-button>
          <el-button type="primary" @click="addVehicle">确 定</el-button>
        </div>
      </el-dialog>
      <el-dialog title="是否确认删除?" :visible.sync="dialogRemoveVisible">
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogRemoveVisible = false">取 消</el-button>
          <el-button type="primary" @click="rmVehicle">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { getVehiclesApi, updateVehicleApi, rmVehicleApi, addVehicleApi } from '@/api/getData'
export default {
  components: {
  },
  data() {
    return {
      // 查询
      listQuery: {
        limit: 20,
        license_plate: undefined,
        phone_number: undefined
      },
      downloadLoading: false,
      offset: 0,
      limit: 20,
      count: 0,
      tableData: [],
      newTable: {},
      currentPage: 1,
      selectTable: {},
      dialogFormVisible: false,
      dialogAddVisible: false,
      dialogRemoveVisible: false,
      expendRow: [],
      rmLicense: undefined
    }
  },
  computed: {
  },
  created() {
  },
  methods: {
    handleFilter() {
      console.log('111')
      getVehiclesApi({
        offset: this.offset,
        limit: this.limit,
        license_plate: this.listQuery.license_plate,
        phone_number: this.listQuery.phone_number
      }).then(vehicles => {
        console.log(vehicles)
        if (vehicles['code'] === 'success') {
          this.count = vehicles.data.count
          this.tableData = vehicles.data.vehicles
          this.$message({
            type: 'success',
            message: '成功获取 ' + this.count + ' 个车辆'
          })
        } else {
          this.$message({
            type: 'error',
            message: '获取数据失败: ' + vehicles['info']
          })
        }
      }).catch(err => {
        console.log(err)
      })
      // const vehicles = {"code": "success", "data": {"count": 5, "vehicles": [{"owner_name": null, "phone_number": null, "license_plate": "\u7696A92141", "addition_info": "", "cards": []}, {"owner_name": null, "phone_number": null, "license_plate": "EL0662", "addition_info": "", "cards": []}, {"owner_name": null, "phone_number": null, "license_plate": "\u664bCV8999", "addition_info": "", "cards": []}, {"owner_name": null, "phone_number": null, "license_plate": "\u4eacNQ4163", "addition_info": "", "cards": []}, {"owner_name": null, "phone_number": null, "license_plate": "\u4eacK98410", "addition_info": "", "cards": []}]}}
    },
    handleAdd() {
      this.dialogAddVisible = true
    },
    async addVehicle() {
      this.dialogAddVisible = false
      try {
        const res = await addVehicleApi(this.newTable)
        if (res.code === 'success') {
          this.$message({
            'type': 'success',
            'message': '添加车辆成功'
          })
        } else {
          this.$message({
            'type': 'error',
            'message': '添加车辆失败: ' + res.info
          })
        }
      } catch (err) {
        this.$message({
          'type': 'error',
          'message': '添加车辆失败: ' + err
        })
      }
    },
    handleRemove(row) {
      this.dialogRemoveVisible = true
      this.rmLicense = row.license_plate
    },
    async rmVehicle() {
      this.dialogRemoveVisible = false
      try {
        const res = await rmVehicleApi({
          'license_plate': this.rmLicense
        })
        if (res.code === 'success') {
          this.$message({
            type: 'success',
            message: '删除车位成功'
          })
        } else {
          this.$message({
            type: 'error',
            message: '删除车位失败: ' + res.info
          })
        }
      } catch (err) {
        console.log(err)
        this.$message({
          type: 'error',
          message: '删除车位失败: ' + err
        })
      }
    },
    handleDownload() {
      this.downloadLoading = true
              import('@/vendor/Export2Excel').then(excel => {
                const tHeader = ['车牌号', '手机号', '持有人姓名', '会员卡信息',
                  '备注']
                const filterVal = ['license_plate', 'phone_number',
                  'owner_name', 'cards', 'addition_info']
                const data = this.formatJson(filterVal, this.tableData)
                excel.export_json_to_excel({
                  header: tHeader,
                  data,
                  filename: 'VehiclesInfo'
                })
                this.downloadLoading = false
              })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'cards') {
          return JSON.stringify(v[j])
        } else {
          return v[j]
        }
      }))
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.offset = (val - 1) * this.limit
      this.handleFilter()
    },
    expand(row, expandedRows) {
      row.used = String(row.used)
      this.selectTable = row
    },
    handleEdit(row) {
      this.dialogFormVisible = true
    },
    async updateVehicle() {
      this.dialogFormVisible = false
      try {
        var postData = this.selectTable
        const res = await updateVehicleApi(postData)
        if (res.code === 'success') {
          this.$message({
            type: 'success',
            message: '更新车辆信息成功'
          })
        } else {
          this.$message({
            type: 'error',
            message: '更新车辆信息失败: ' + res.info
          })
        }
      } catch (err) {
        console.log('更新车辆信息失败', err)
      }
    }
  }
}
</script>

<style>
    .demo-table-expand {
        font-size: 0;
    }
    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }
    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 50%;
    }
    .table_container{
        padding: 20px;
    }
    .Pagination{
        display: flex;
        justify-content: flex-start;
        margin-top: 8px;
    }
    .avatar-uploader .el-upload {
        border: 1px dashed #d9d9d9;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .avatar-uploader .el-upload:hover {
        border-color: #20a0ff;
    }
    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 120px;
        height: 120px;
        line-height: 120px;
        text-align: center;
    }
    .avatar {
        width: 120px;
        height: 120px;
        display: block;
    }
</style>
