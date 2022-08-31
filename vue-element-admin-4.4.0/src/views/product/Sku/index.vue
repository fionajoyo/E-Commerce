<template>
  <div>
    <!-- 表格 -->
    <el-table style="width: 100%" :data="records" border>
      <el-table-column type="index" label="序号" width="80" align="center">
      </el-table-column>
      <el-table-column prop="skuName" label="名称" width="width">
      </el-table-column>
      <el-table-column prop="skuDesc" label="描述" width="width">
      </el-table-column>
      <el-table-column label="默认图片" width="110">
        <template slot-scope="{ row, $index }">
          <img :src="row.skuDefaultImg" alt="" style="width: 90px" />
        </template>
      </el-table-column>
      <el-table-column prop="weight" label="重量(KG)" width="80">
      </el-table-column>
      <el-table-column prop="price" label="价格(元)" width="80">
      </el-table-column>
      <el-table-column prop="prop" label="操作" width="width">
        <template slot-scope="{ row, $index }">
          <!-- 上架按钮 -->
          <el-button
            type="success"
            icon="el-icon-bottom"
            size="mini"
            v-if="row.isSale == 0"
            @click="sale(row)"
          ></el-button>
          <!-- 下架按按钮 -->
          <el-button
            type="info"
            icon="el-icon-top"
            size="mini"
            @click="cancelSale(row)"
            v-else
          ></el-button>
          <!-- 编辑按钮 -->
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            @click="edit"
          ></el-button>
          <!-- 查看按钮 -->
          <el-button
            type="info"
            icon="el-icon-info"
            size="mini"
            @click="getSkuInfo(row)"
          ></el-button>
          <!-- 删除按钮 -->
          <el-button
            type="danger"
            icon="el-icon-delete"
            size="mini"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页器 -->
    <el-pagination
      style="text-align: center"
      :current-page="1"
      :page-sizes="[3, 5, 10]"
      :page-size="5"
      layout="prev, pager, next, jumper,->,sizes,total"
      :total="20"
      @current-change="getSkuList"
      @size-change="handleSizeChange"
    >
    </el-pagination>
    <!-- 抽屉效果 -->
    <el-drawer
      :visible.sync="drawer"
      :direction="direction"
      :show-close="false"
      size="50%"
    >
      <el-row>
        <el-col :span="5">名称</el-col>
        <el-col :span="16">{{ skuInfo.skuName }}</el-col>
      </el-row>
      <el-row>
        <el-col :span="5">描述</el-col>
        <el-col :span="16">{{ skuInfo.skuDesc }}</el-col>
      </el-row>
      <el-row>
        <el-col :span="5">价格</el-col>
        <el-col :span="16">{{ skuInfo.price }}元</el-col>
      </el-row>
      <el-row>
        <el-col :span="5">平台属性</el-col>
        <el-col :span="16">
          <template>
            <el-tag
              type="success"
              v-for="(attr, index) in skuInfo.skuAttrValueList"
              :key="attr.id"
              style="margin-right: 10px; margin-bottom: 5px"
            >
              {{ attr.attrId }}-{{ attr.valueId }}
            </el-tag>
          </template>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="5">商品图片</el-col>
        <el-col :span="16">
          <el-carousel indicator-position="outside">
            <el-carousel-item
              v-for="item in skuInfo.skuImageList"
              :key="item.id"
            >
              <img
                :src="item.imgUrl"
                alt=""
                style="
                  display: block;
                  height: 100%;
                  margin-left: auto;
                  margin-right: auto;
                "
              />
            </el-carousel-item>
          </el-carousel> </el-col></el-row
    ></el-drawer>
  </div>
</template>
        </el-col>
      </el-row>
    </el-drawer>
  </div>
</template>

<script>
export default {
  name: "sku",
  data() {
    return {
      // 当前第几页
      page: 1,
      // 代表当前页面有几条数据
      limit: 5,
      // 分页器一共展示的数据
      total: 0,
      // sku列表的数据
      records: [],
      // sku详情信息
      skuInfo: {},
      // 抽屉的显示与隐藏
      drawer: false,
      // 控制抽屉的方向
      direction: "rtl",
    };
  },
  mounted() {
    // 获取sku列表
    this.getSkuList();
  },
  methods: {
    // 获取sku列表数据
    async getSkuList(pages = 1) {
      this.page = pages;
      const { page, limit } = this;
      let result = await this.$API.sku.reqSkuList(page, limit);
      if (result.code === 200) {
        this.total = result.data.total;
        this.records = result.data.records;
      }
    },
    // 每一页条数发生变化是
    handleSizeChange(limit) {
      this.limit = limit;
      this.getSkuList();
    },
    // 上架商品
    async sale(row) {
      let result = await this.$API.sku.reqSale(row.id);
      if (result.code === 200) {
        row.isSale = 1;
        this.$message({ type: "success", message: "上架商品成功" });
      }
    },
    // 下架商品
    async cancelSale(row) {
      let result = await this.$API.sku.reqCancel(row.id);
      if (result.code === 200) {
        row.isSale = 0;
        this.$message({ type: "info", message: "下架商品成功" });
      }
    },
    // 编辑按钮回调
    edit() {
      this.$message({ type: "info", message: "正在开发中......" });
    },
    // 获取Sku详情
    async getSkuInfo(sku) {
      // 打开抽屉
      this.drawer = true;

      let result = await this.$API.sku.reqSkuById(sku.id);
      if (result.code === 200) {
        this.skuInfo = result.data;
      }
    },
  },
};
</script>

<style>
.el-row .el-col-5 {
  font-size: 18px;
  text-align: right;
}
.el-col {
  margin: 10px;
}
</style>