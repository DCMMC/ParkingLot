<template>
  <div class="fillcontain">
    <div class="filter-container">
      <el-input v-model="listQuery.license_plate" :placeholder="'车牌号'" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-date-picker
        v-model="listQuery.date_in_start"
        type="datetime"
        format="yyyy/MM/dd, HH:mm:ss"
        value-format="yyyy/MM/dd, HH:mm:ss"
        placeholder="选择入场开始日期时间"
      />
      <el-date-picker
        v-model="listQuery.date_in_end"
        format="yyyy/MM/dd, HH:mm:ss"
        value-format="yyyy/MM/dd, HH:mm:ss"
        type="datetime"
        placeholder="选择入场结束日期时间"
      />
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
        :row-key="row => row.date_in"
        style="width: 100%"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="车牌号" label-width="160px">
                <span>{{ props.row.license_plate }}</span>
              </el-form-item>
              <el-form-item label="入场时间" label-width="160px">
                <span>{{ props.row.date_in }}</span>
              </el-form-item>
              <el-form-item label="入口" label-width="160px">
                <span>{{ props.row.indoor }}</span>
              </el-form-item>
              <el-form-item label="出场时间" label-width="160px">
                <span>{{ props.row.date_out }}</span>
              </el-form-item>
              <el-form-item label="出口" label-width="160px">
                <span>{{ props.row.outdoor }}</span>
              </el-form-item>
              <el-form-item label="收取费用" label-width="160px">
                <span>{{ props.row.fee }}</span>
              </el-form-item>
              <el-form-item
                v-if="props.row.card_id && props.row.card_id !== ''"
                label="会员卡卡号"
                label-width="160px"
              >
                <span>{{ props.row.card_id }}</span>
              </el-form-item>
              <el-form-item
                v-if="props.row.card_id && props.row.card_id !== ''"
                label="会员卡类型"
                label-width="160px"
              >
                <span>{{ props.row.card_type }}</span>
              </el-form-item>
              <el-form-item label="备注" label-width="160px">
                <span>{{ props.row.addition_info }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="车牌号"
          prop="parking_id"
        />
        <el-table-column
          label="费用"
          prop="fee"
        />
        <el-table-column
          label="入场时间"
          prop="date_in"
        />
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
    </div>
  </div>
</template>

<script>
import { getBillLog } from '@/api/getData'
export default {
  components: {},
  data() {
    return {
      // 查询
      listQuery: {
        license_plate: undefined,
        date_in_start: undefined,
        date_in_end: undefined
      },
      downloadLoading: false,
      offset: 0,
      limit: 20,
      count: 0,
      tableData: [],
      currentPage: 1
    }
  },
  computed: {
  },
  created() {
  },
  methods: {
    async handleFilter() {
      try {
        const parkings = await getBillLog({
          offset: this.offset,
          limit: this.limit,
          license_plate: this.listQuery.license_plate,
          date_in_start: this.listQuery.date_in_start,
          date_in_end: this.listQuery.date_in_end
        })
        // const parkings = {"code": "success", "data": {"parkings": [{"addition_info": "1", "parking_id": "1", "floor_id": "1", "region_id": "1", "status": "normal", "used": false}], "count": 1}}
        if (parkings['code'] === 'success') {
          this.count = parkings.data.count
          this.tableData = parkings.data.logs
          this.$message({
            type: 'success',
            message: '获取数据成功: ' + this.count
          })
        } else {
          this.$message({
            type: 'error',
            message: '获取数据失败: ' + parkings['info']
          })
        }
      } catch (err) {
        console.log(err)
      }
    },
    handleDownload() {
      this.downloadLoading = true
              import('@/vendor/Export2Excel').then(excel => {
                const tHeader = ['车牌', '入场时间',
                  '入口', '出场时间', '出口', '费用', '备注']
                const filterVal = ['license_plate', 'date_in', 'indoor',
                  'date_out', 'outdoor', 'outdoor', 'fee', 'addition_info']
                const data = this.formatJson(filterVal, this.tableData)
                excel.export_json_to_excel({
                  header: tHeader,
                  data,
                  filename: 'ParkingInfo'
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
