<template>
  <div class="fillcontain">
    <div class="filter-container">
      <el-input v-model="listQuery.card_id" :placeholder="'会员卡号'" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.license_plate" :placeholder="'绑定车牌号'" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleAdd">
        新增会员卡
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
              <el-form-item label="会员卡号" label-width="160px">
                <span>{{ props.row.card_id }}</span>
              </el-form-item>
              <el-form-item label="会员卡类型" label-width="160px">
                <span>{{ props.row.card_type }}</span>
              </el-form-item>
              <el-form-item label="会员卡余额" label-width="160px">
                <span>{{ props.row.value }}</span>
              </el-form-item>
              <el-form-item
                v-for="v in props.row.bind_vehicles"
                :key="v.license_plate"
                :label="'绑定车辆'"
              >
                车牌号: {{ card.license_plate }}
              </el-form-item>
              <el-form-item label="备注" label-width="160px">
                <span>{{ props.row.addition_info }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="卡号"
          prop="card_id"
        />
        <el-table-column
          label="绑定手机号"
          prop="phone_number"
        />
        <el-table-column
          label="会员卡类型"
          prop="card_type"
        />
        <el-table-column label="操作" width="260">
          <template slot-scope="scope">
            <el-button
              size="small"
              @click="handleEdit(scope.row)"
            >编辑</el-button>
            <el-button class="filter-item" type="danger" size="small" icon="el-icon-search" @click="handleRemove(scope.row)">
              删除会员卡
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
      <el-dialog title="修改停会员卡信息" :visible.sync="dialogFormVisible">
        <el-form :model="selectTable">
          <el-form-item label="会员卡号" label-width="400px">
            <el-input
              v-model="selectTable.card_id"
              auto-complete="off"
              :disable="true"
            />
          </el-form-item>
          <el-form-item label="会员卡余额" label-width="400px">
            <el-input v-model="selectTable.value" auto-complete="off" />
          </el-form-item>
          <el-form-item label="手机号" label-width="400px">
            <el-input v-model="selectTable.phone_number" />
          </el-form-item>
          <!-- TODO 删除绑定车牌 -->
          <el-form-item label="添加绑定车牌" label-width="400px">
            <el-input v-model="selectTable.bind_license" />
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
          <el-form-item label="会员卡类型(储值卡top-up, 记次卡count)" label-width="400px">
            <el-input v-model="newTable.card_type" auto-complete="off" />
          </el-form-item>
          <el-form-item label="会员卡余额" label-width="400px">
            <el-input v-model="newTable.value" auto-complete="off" />
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
import { getMemberCardApi, updateMemberCardApi, rmMemberCardApi, addMemberCardApi } from '@/api/getData'
export default {
  components: {
  },
  data() {
    return {
      // 查询
      listQuery: {
        limit: 20,
        license_plate: undefined,
        card_id: undefined
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
      rmCardId: undefined
    }
  },
  computed: {
  },
  created() {
  },
  methods: {
    handleFilter() {
      getMemberCardApi({
        offset: this.offset,
        limit: this.limit,
        license_plate: this.listQuery.license_plate,
        card_id: this.listQuery.card_id
      }).then(card => {
        if (card['code'] === 'success') {
          this.count = card.data.count
          this.tableData = card.data.cards
          this.$message({
            type: 'success',
            message: '成功获取 ' + this.count + ' 张会员卡'
          })
        } else {
          this.$message({
            type: 'error',
            message: '获取数据失败: ' + card['info']
          })
        }
      }).catch(err => {
        console.log(err)
      })
    },
    handleAdd() {
      this.dialogAddVisible = true
    },
    async addVehicle() {
      this.dialogAddVisible = false
      try {
        const res = await addMemberCardApi(this.newTable)
        if (res.code === 'success') {
          this.$message({
            'type': 'success',
            'message': '添加会员卡成功'
          })
        } else {
          this.$message({
            'type': 'error',
            'message': '添加会员卡失败: ' + res.info
          })
        }
      } catch (err) {
        this.$message({
          'type': 'error',
          'message': '添加会员卡失败: ' + err
        })
      }
    },
    handleRemove(row) {
      this.dialogRemoveVisible = true
      this.rmCardId = row.card_id
    },
    async rmVehicle() {
      this.dialogRemoveVisible = false
      try {
        const res = await rmMemberCardApi({
          'card_id': this.rmCardId
        })
        if (res.code === 'success') {
          this.$message({
            type: 'success',
            message: '删除会员卡成功'
          })
        } else {
          this.$message({
            type: 'error',
            message: '删除会员卡失败: ' + res.info
          })
        }
      } catch (err) {
        console.log(err)
        this.$message({
          type: 'error',
          message: '删除会员卡失败: ' + err
        })
      }
    },
    handleDownload() {
      this.downloadLoading = true
              import('@/vendor/Export2Excel').then(excel => {
                const tHeader = ['会员卡号', '手机号', '会员卡类型',
                  '会员卡余额', '备注']
                const filterVal = ['card_id', 'phone_number',
                  'card_type', 'value', 'addition_info']
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
        return v[j]
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
        const res = await updateMemberCardApi(postData)
        if (res.code === 'success') {
          this.$message({
            type: 'success',
            message: '更新会员卡信息成功'
          })
        } else {
          this.$message({
            type: 'error',
            message: '更新会员卡信息失败: ' + res.info
          })
        }
      } catch (err) {
        console.log('更新会员卡信息失败', err)
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
