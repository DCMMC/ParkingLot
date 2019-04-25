<template>
  <div class="fillcontain">
    <div class="filter-container">
      <el-input v-model="listQuery.parking_id" :placeholder="'停车位id'" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.region_id" :placeholder="'区域id'" style="width: 130px" class="filter-item">
        <el-option
          v-for="item in {'1': {'id': '1', 'name': '一层'}}"
          :key="item.id"
          :label="item.id + '(' + item.name + ')'"
          :value="item.id"
        />
      </el-select>
      <el-select v-model="listQuery.floor_id" :placeholder="'楼层id'" class="filter-item" style="width: 130px">
        <el-option
          v-for="item in {'1': {'id': '1', 'name': '一区'}}"
          :key="item.id"
          :label="item.id + '(' + item.name + ')'"
          :value="item.id"
        />
      </el-select>
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
        :row-key="row => row.parking_id"
        style="width: 100%"
        @expand-change="expand"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="停车位id" label-width="160px">
                <span>{{ props.row.parking_id }}</span>
              </el-form-item>
              <el-form-item label="楼层id" label-width="160px">
                <span>{{ props.row.floor_id }}</span>
              </el-form-item>
              <el-form-item label="区域id" label-width="160px">
                <span>{{ props.row.region_id }}</span>
              </el-form-item>
              <el-form-item label="车位可用状态" label-width="160px">
                <span>{{ props.row.status_zh }}</span>
              </el-form-item>
              <el-form-item label="车位使用情况" label-width="160px">
                <span>{{ props.row.used_zh }}</span>
              </el-form-item>
              <el-form-item label="备注" label-width="160px">
                <span>{{ props.row.addition_info }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="停车位id"
          prop="parking_id"
        />
        <el-table-column
          label="楼层id"
          prop="floor_id"
        />
        <el-table-column
          label="区域id"
          prop="region_id"
        />
        <el-table-column label="操作" width="160">
          <template slot-scope="scope">
            <el-button
              size="small"
              @click="handleEdit(scope.row)"
            >编辑</el-button>
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
      <el-dialog title="修改停车位信息" :visible.sync="dialogFormVisible">
        <el-form :model="selectTable">
          <el-form-item label="车位号" label-width="400px">
            <el-input
              v-model="selectTable.parking_id"
              auto-complete="off"
              :disable="true"
            />
          </el-form-item>
          <el-form-item label="车位可用状态('normal'(正常使用), 'unavailable'(不可用, e.g., 正在维修))" label-width="400px">
            <el-input v-model="selectTable.status" auto-complete="off" />
          </el-form-item>
          <el-form-item label="车位使用情况('true'正在使用, 'false'未被使用)" label-width="400px">
            <el-input v-model="selectTable.used" />
          </el-form-item>
          <el-form-item label="备注信息" label-width="400px">
            <el-input v-model="selectTable.addition_info" />
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="updateParking">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { getParkings, updateParkingApi } from '@/api/getData'
export default {
  components: {},
  data() {
    return {
      // 查询
      listQuery: {
        limit: 20,
        parking_id: undefined,
        floor_id: undefined,
        region_id: undefined
      },
      downloadLoading: false,
      offset: 0,
      limit: 20,
      count: 0,
      tableData: [],
      currentPage: 1,
      selectTable: {},
      dialogFormVisible: false,
      expendRow: []
    }
  },
  computed: {
  },
  created() {
  },
  methods: {
    async handleFilter() {
      try {
        console.log('handleFilter')
        const parkings = await getParkings({
          offset: this.offset,
          limit: this.limit,
          parking_id: this.listQuery.parking_id,
          region_id: this.listQuery.region_id,
          floor_id: this.listQuery.floor_id
        })
        console.log('getParkings')
        console.log(parkings)
        // const parkings = {"code": "success", "data": {"parkings": [{"addition_info": "1", "parking_id": "1", "floor_id": "1", "region_id": "1", "status": "normal", "used": false}], "count": 1}}
        if (parkings['code'] === 'success') {
          this.count = parkings.data.count
          parkings.data.parkings.forEach((v, i) => {
            var status_zh = ''
            switch (v.status) {
              case 'normal': status_zh = '正常'; break
              case 'unavailable': status_zh = '不可用(可能正在维护中)'; break
              case 'obligated': status_zh = '特殊情况预留(e.g., 已预约'; break
              default: status_zh = status
            }
            parkings.data.parkings[i]['status_zh'] = status_zh
            var used_zh = ''
            if (v.used) {
              used_zh = '正在使用中'
            } else {
              used_zh = '空车位'
            }
            parkings.data.parkings[i]['used'] = String(v.used)
            parkings.data.parkings[i]['used_zh'] = used_zh
          })
          this.tableData = parkings.data.parkings
        } else {
          this.$message({
            type: 'error',
            message: '获取数据失败: ' + parkings['info']
          })
        }
      } catch (e) {
        console.log(e)
      }
    },
    handleDownload() {
      this.downloadLoading = true
              import('@/vendor/Export2Excel').then(excel => {
                const tHeader = ['停车位id', '楼层id', '区域id', '状态信息',
                  '可用信息', '备注']
                const filterVal = ['parking_id', 'floor_id', 'region_id',
                  'status', 'used', 'addition_info']
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
    },
    expand(row, expandedRows) {
      row.used = String(row.used)
      this.selectTable = row
    },
    handleEdit(row) {
      this.dialogFormVisible = true
    },
    async updateParking() {
      this.dialogFormVisible = false
      try {
        var postData = this.selectTable
        postData.used = (postData.used !== 'false')
        const res = await updateParkingApi(postData)
        if (res.code === 'success') {
          this.$message({
            type: 'success',
            message: '更新停车位信息成功'
          })
          this.getFoods()
        } else {
          this.$message({
            type: 'error',
            message: '更新停车位信息失败: ' + res.info
          })
        }
      } catch (err) {
        console.log('更新停车位信息失败', err)
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
