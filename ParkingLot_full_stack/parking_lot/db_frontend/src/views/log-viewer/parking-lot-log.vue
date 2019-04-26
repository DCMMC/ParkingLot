<template>
  <div class="fillcontain">
    <div class="filter-container">
      <el-select v-model="listQuery.event_type" :placeholder="'事件类型'" style="width: 130px" class="filter-item">
        <el-option
          v-for="item, key in {'车位状态更新': 'update_parking'}"
          :key="item"
          :label="item"
          :value="key"
        />
      </el-select>
      <el-date-picker
        v-model="listQuery.date_start"
        type="datetime"
        format="yyyy/MM/dd, HH:mm:ss"
        value-format="yyyy/MM/dd, HH:mm:ss"
        placeholder="选择开始日期时间"
      />
      <el-date-picker
        v-model="listQuery.date_end"
        type="datetime"
        format="yyyy/MM/dd, HH:mm:ss"
        value-format="yyyy/MM/dd, HH:mm:ss"
        placeholder="选择结束日期时间"
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
              <el-form-item label="事件类型" label-width="160px">
                <span>{{ props.row.event_type }}</span>
              </el-form-item>
              <el-form-item label="时间" label-width="160px">
                <span>{{ props.row.date_created }}</span>
              </el-form-item>
              <el-form-item label="操作管理员" label-width="160px">
                <span>{{ props.row.admin_info }}</span>
              </el-form-item>
              <el-form-item label="备注" label-width="160px">
                <span>{{ props.row.event_info }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="事件类型"
          prop="event_type"
        />
        <el-table-column
          label="时间"
          prop="date_created"
        />
        <el-table-column
          label="操作管理员"
          prop="admin_info"
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
import { getParkingLotLog } from '@/api/getData'
export default {
  components: {},
  data() {
    return {
      // 查询
      listQuery: {
        event_type: undefined,
        date_start: undefined,
        date_end: undefined
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
        const parkings = await getParkingLotLog({
          offset: this.offset,
          limit: this.limit,
          event_type: this.listQuery.event_type,
          date_start: this.listQuery.date_start,
          date_end: this.listQuery.date_end
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
                const tHeader = ['事件类型', '时间', '操作管理员',
                  '状态信息', '关联信息', '备注']
                const filterVal = ['event_type', 'date_created',
                  'admin_info', 'event_info']
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
