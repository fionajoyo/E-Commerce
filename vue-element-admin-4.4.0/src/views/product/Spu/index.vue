<template>
  <div>
    <!-- 三级联动 -->
    <el-card style="margin: 20px 0">
      <categorySelect
        @getCategoryId="getCategoryId"
        :show="scene != 0"
      ></categorySelect>
    </el-card>

    <!-- spu列表展示修改与更新 -->
    <el-card>
      <!-- spu列表展示 -->
      <div v-show="scene == 0">
        <!-- 添加spu属性 -->
        <el-button
          type="primary"
          icon="el-icon-plus"
          :disabled="!category3Id"
          @click="addSpu"
        >
          添加SPU
        </el-button>
        <!-- spu数据列表 -->
        <el-table style="width: 100%; margin: 10px 0" border :data="records">
          <el-table-column type="index" label="序号" width="80" align>
          </el-table-column>
          <el-table-column prop="spuName" label="SPU名称" width="width">
          </el-table-column>
          <el-table-column prop="description" label="SPU描述" width="width">
          </el-table-column>
          <el-table-column prop="prop" label="操作" width="width">
            <template slot-scope="{ row, $index }">
              <!-- 新增sku属性按钮 -->
              <el-button
                type="success"
                icon="el-icon-plus"
                size="mini"
                title="新增"
                @click="addSku(row)"
              ></el-button>
              <!-- 修改按钮 -->
              <el-button
                type="warning"
                icon="el-icon-edit"
                size="mini"
                title="修改"
                @click="changeSku(row)"
              ></el-button>
              <!-- 查看按钮 -->
              <el-button
                type="info"
                icon="el-icon-info"
                size="mini"
                title="查看"
                @click="handler(row)"
              ></el-button>
              <!-- 删除按钮 -->
              <el-popconfirm
                @onConfirm="deleteSpu(row)"
                title="这是一段内容确定删除吗？"
              >
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  title="删除"
                  style="margin-left: 10px"
                  slot="reference"
                ></el-button>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页器 -->
        <el-pagination
          style="text-align: center"
          :current-page="page"
          :page-sizes="[3, 5, 10]"
          :page-size="limit"
          layout="prev, pager, next, jumper,->,sizes,total"
          :total="total"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
        >
        </el-pagination>
      </div>
      <!-- 添加SPU|修改SPU -->
      <SpuForm
        v-show="scene == 1"
        @changeScene="changeScene"
        ref="spu"
      ></SpuForm>
      <!-- 添加SKU -->
      <SkuForm
        v-show="scene == 2"
        ref="sku"
        @changeScenes="changeScenes"
      ></SkuForm>
      <!-- sku信息展示对话框 -->
      <el-dialog
        :title="`${spu.spuName}的sku列表`"
        :visible.sync="dialogTableVisible"
        :before-close="closeDialog"
      >
        <el-table :data="skuList" v-loading="loading">
          <el-table-column
            prop="skuName"
            label="名称"
            width="width"
          ></el-table-column>
          <el-table-column
            prop="price"
            label="价格"
            width="width"
          ></el-table-column>
          <el-table-column
            prop="weight"
            label="重量"
            width="width"
          ></el-table-column>
          <el-table-column label="默认图片" width="width">
            <template slot-scope="{ row, $index }">
              <img :src="row.skuDefaultImg" alt="" style="width: 100px" />
            </template>
          </el-table-column>
        </el-table>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
// 引入子组件
import SpuForm from "./SpuForm";
import SkuForm from "./SkuForm";

export default {
  name: "spu",
  data() {
    return {
      // 控制三级联动可操作性
      isShowTable: true,
      // 菜单一级id
      category1Id: "",
      // 菜单二级id
      category2Id: "",
      // 菜单三级id
      category3Id: "",
      // spu列表属性当前页码
      page: 1,
      // 每一页展示多少数据
      limit: 3,
      // spu数据列表
      records: [],
      // 分页器一共要展示数据的条数
      total: 0,
      // 切换场景，0代表展示spu列表数据,1代表添加|修改SPU，2代表添加SKU
      scene: 0,
      // 控制sku信息对话框的显示与隐藏
      dialogTableVisible: false,
      // spu数据
      spu: {},
      // sku数据
      skuList: [],
      // 加载动画
      loading: true,
    };
  },
  methods: {
    // 三级联动自定义事件，回传选中的三级ID
    getCategoryId({ category1Id, category2Id, category3Id }) {
      this.category1Id = category1Id;
      this.category2Id = category2Id;
      this.category3Id = category3Id;
      if (category3Id) {
        this.getSpuList();
      } else {
        // 清除当前页展示的数据（没有3ID）
        this.records = [];
      }
    },
    // 获取spu列表数据的方法
    async getSpuList() {
      const { page, limit, category3Id } = this;
      let result = await this.$API.spu.reqSpuList(page, limit, category3Id);
      if (result.code === 200) {
        this.records = result.data.records;
        this.total = result.data.total;
      }
    },
    // 点击分页器页数按钮回调
    handleCurrentChange(page) {
      this.page = page;
      this.getSpuList();
    },
    // 切换分页器展示数据条数
    handleSizeChange(limit) {
      this.limit = limit;
      this.getSpuList();
    },
    // 添加Spu按钮回调
    addSpu() {
      this.scene = 1;
      // 通知子组件发送请求
      this.$refs.spu.addSpuData(this.category3Id);
    },
    // 修改Spu按钮
    changeSku(row) {
      this.scene = 1;
      //获取子组件SpuForm子组件的
      //在父组件当中可以通过$ref获取子组件等等
      this.$refs.spu.initSpuData(row);
    },
    // SpuForm自定义事件回调
    changeScene(scene) {
      // 切换场景
      this.scene = scene;
      // 重新获取spu数据
      this.getSpuList();
    },
    // skuForm自定义事件回调
    changeScenes(scene) {
      // 切换场景
      this.scene = scene;
    },
    // 删除spu按钮回调
    async deleteSpu(row) {
      let result = await this.$API.spu.reqDeleteSpu(row.id);
      if (result.code === 200) {
        this.$message({ type: "success", message: "删除成功" });
        // 重新获取列表数据
        this.getSpuList();
      }
    },
    // 添加sku按钮回调
    addSku(row) {
      // 切换场景为2
      this.scene = 2;
      // 父组件调用子组件方法，让子组件发送请求
      this.$refs.sku.getData(this.category1Id, this.category2Id, row);
    },
    // 查看sku按钮回调
    async handler(spu) {
      // 弹出对话框
      this.dialogTableVisible = true;

      this.spu = spu;
      // 获取sku列表数据
      let result = await this.$API.spu.reqSkuList(spu.id);
      if (result.code === 200) {
        this.skuList = result.data;
        this.loading = false;
      }
    },
    // 关闭sku信息对话框回调
    closeDialog(done) {
      // 重置loading
      this.loading = true;
      // 清除sku信息
      this.skuList = [];
      // 关闭对话框
      done();
    },
  },
  components: {
    SpuForm,
    SkuForm,
  },
};
</script>

<style>
</style>