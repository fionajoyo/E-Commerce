<template>
  <div>
    <el-form ref="form" label-width="80px" :model="spu">
      <el-form-item label="SPU名称">
        <el-input placeholder="SPU名称" v-model="spu.spuName"></el-input>
      </el-form-item>
      <el-form-item label="品牌">
        <el-select placeholder="请选择品牌" v-model="spu.tmId">
          <el-option
            :label="tm.tmName"
            :value="tm.id"
            v-for="(tm, index) in tradeMarkList"
            :key="tm.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="SPU描述">
        <el-input
          type="textarea"
          placeholder="SPU描述"
          v-model="spu.description"
        ></el-input>
      </el-form-item>
      <el-form-item label="SPU图片">
        <el-upload
          action="/dev-api/admin/product/fileUpload"
          list-type="picture-card"
          :on-preview="handlePictureCardPreview"
          :on-remove="handleRemove"
          :file-list="spuImageList"
          :on-success="handlerSuccess"
        >
          <i class="el-icon-plus"></i>
        </el-upload>
        <!-- 预览 -->
        <el-dialog :visible.sync="dialogVisible">
          <img width="100%" :src="dialogImageUrl" alt="" />
        </el-dialog>
      </el-form-item>
      <el-form-item label="销售属性">
        <!-- 选择添加销售属性 -->
        <el-select
          v-model="attrIdAndAttrName"
          :placeholder="`还有${unselectSaleAttr.length}项未选择`"
        >
          <el-option
            :label="unselect.name"
            :value="`${unselect.id}:${unselect.name}`"
            v-for="(unselect, index) in unselectSaleAttr"
            :key="unselect.id"
          ></el-option>
        </el-select>
        <!-- 添加销售属性按钮 -->
        <el-button
          type="primary"
          icon="el-icon-plus"
          style="margin-left: 5px"
          :disabled="!attrIdAndAttrName"
          @click="addSaleAttr"
        >
          添加销售属性
        </el-button>
        <!-- 销售属性列表展示 -->
        <el-table style="width: 100%" :data="spu.spuSaleAttrList" border>
          <el-table-column
            type="index"
            label="序号"
            width="80px"
            align="center"
          >
          </el-table-column>
          <el-table-column prop="saleAttrName" label="属性名" width="width">
          </el-table-column>
          <el-table-column prop="prop" label="属性值名称列表" width="width">
            <template slot-scope="{ row, $index }">
              <!-- 展示属性值 -->
              <el-tag
                :key="tag.id"
                v-for="(tag, index) in row.spuSaleAttrValueList"
                closable
                @close="handleClose(row, index)"
                :disable-transitions="false"
              >
                {{ tag.saleAttrValueName }}
              </el-tag>
              <!-- 输入框 -->
              <el-input
                class="input-new-tag"
                v-if="row.inputVisible"
                v-model="row.inputValue"
                :ref="`${$index}`"
                size="small"
                @keyup.enter.native="handleInputConfirm"
                @blur="handleInputConfirm(row)"
                style="margin: 5px 5px"
              >
              </el-input>
              <!-- 添加按钮 -->
              <el-button
                v-else
                class="button-new-tag"
                size="small"
                @click="showInput(row, $index)"
                style="margin: 5px 5px"
              >
                添加
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="prop" label="操作" width="width">
            <template slot-scope="{ row, $index }">
              <!-- 删除按钮 -->
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                @click="spu.spuSaleAttrList.splice($index, 1)"
              ></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-form-item>
      <!-- 操作 -->
      <el-form-item>
        <el-button type="primary" @click="addOrUpdateSpu">保存</el-button>
        <el-button @click="switchScene">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "SpuForm",
  data() {
    return {
      // 照片墙的两个数据
      dialogImageUrl: "",
      dialogVisible: false,
      // 存储spu数据
      spu: {
        //三级分类的id
        category3Id: 0,
        //描述
        description: "",
        //spu名称
        spuName: "",
        //平台的id
        tmId: "",
        //收集SPU图片的信息
        spuImageList: [
          // {
          //   id: 0,
          //   imgName: "string",
          //   imgUrl: "string",
          //   spuId: 0,
          // },
        ],
        //平台属性与属性值收集
        spuSaleAttrList: [
          // {
          //   baseSaleAttrId: 0,
          //   id: 0,
          //   saleAttrName: "string",
          //   spuId: 0,
          //   spuSaleAttrValueList: [
          //     {
          //       baseSaleAttrId: 0,
          //       id: 0,
          //       isChecked: "string",
          //       saleAttrName: "string",
          //       saleAttrValueName: "string",
          //       spuId: 0,
          //     },
          //   ],
          // },
        ],
      },
      // 存放品牌数据
      tradeMarkList: [],
      // 存放平台中全部销售属性
      saleAttrList: [],
      // 收集选择的销售属性id
      attrIdAndAttrName: "",
      // 图片
      spuImageList: [],
    };
  },
  methods: {
    // 删除照片墙图片
    handleRemove(file, fileList) {
      this.spuImageList = fileList;
    },
    // 照片墙图片预览
    handlePictureCardPreview(file) {
      // 传递预览图片地址
      this.dialogImageUrl = file.url;
      // 对话框（预览）显示
      this.dialogVisible = true;
    },
    // 图片上传成功
    handlerSuccess(res, file, fileList) {
      this.spuImageList = fileList;
    },
    // 初始化spu数据
    async initSpuData(spu) {
      // 发送请求
      // 获取spu信息的数据
      let spuResult = await this.$API.spu.reqSpu(spu.id);
      // 获取品牌数据
      let tradeMarkResult = await this.$API.spu.reqTrademarkList();
      // 获取图片列表
      let spuImageResult = await this.$API.spu.reqSpuImageList(spu.id);
      // 获取平台中全部销售属性
      let baseSaleAttrResult = await this.$API.spu.reqBaseSaleAttrList();

      if (spuResult.code == 200) {
        // 存储数据
        this.spu = spuResult.data;
      } else {
        this.$message({ type: "error", message: "获取spu信息失败！" });
      }

      if (tradeMarkResult.code == 200) {
        // 存放数据
        this.tradeMarkList = tradeMarkResult.data;
      } else {
        this.$message({ type: "error", message: "获取品牌信息失败！" });
      }

      if (spuImageResult.code == 200) {
        // 存放数据
        // 整理数据
        let listArr = spuImageResult.data;
        listArr.forEach((element) => {
          element.name = element.imgName;
          element.url = element.imgUrl;
        });
        this.spuImageList = listArr;
      } else {
        this.$message({ type: "error", message: "获取图片信息失败！" });
      }

      if (baseSaleAttrResult.code == 200) {
        // 存放数据
        this.saleAttrList = baseSaleAttrResult.data;
      } else {
        this.$message({ type: "error", message: "获取销售属性信息失败！" });
      }
    },
    // 切换场景（取消按钮）
    switchScene() {
      // 将原有的数据置空
      // Object.assign：es6中新增的方法，可以合并对象
      // 组件实例this._data，可以操作data当中响应式数据
      // 组件实例this.$options：当前组件的配置对象
      Object.assign(this._data, this.$options.data());

      this.$emit("changeScene", 0);
    },
    // 删除属性值
    handleClose(row, index) {
      row.spuSaleAttrValueList.splice(index, 1);
    },
    // 添加属性值
    showInput(row, index) {
      //挂载在销售属性身上的响应式数据inputVisible，控制button与input切换
      if (!row.inputVisible) {
        this.$set(row, "inputVisible", true);
      } else {
        row.inputVisible = true;
      }

      //通过响应式数据inputValue字段收集新增的销售属性值
      if (!row.inputValue) {
        this.$set(row, "inputValue", "");
      } else {
        row.inputValue = "";
      }
      // 聚焦input框
      this.$nextTick(() => {
        this.$refs[index].focus();
      });
    },
    // 添加属性值输入框确认操作
    handleInputConfirm(row) {
      // 结构出销售属性中的数据
      const { baseSaleAttrId, inputValue } = row;
      // 新增销售属性值的名称不能为空
      if (inputValue.trim() == "") {
        this.$message({ type: "warning", message: "输入不能为空!" });
        return;
      }
      // 新增销售属性值不能重复
      if (
        !row.spuSaleAttrValueList.every(
          (item) => item.saleAttrValueName != inputValue
        )
      ) {
        this.$message({ type: "warning", message: "输入不能重复!" });
        return;
      }

      let newSaleAttrValue = {
        baseSaleAttrId,
        saleAttrValueName: inputValue,
      };
      // 添加新的属性值
      row.spuSaleAttrValueList.push(newSaleAttrValue);

      // 隐藏输入框
      row.inputVisible = false;
      row.inputValue = "";
    },
    // 添加新的销售属性
    addSaleAttr() {
      // 把收集到的销售属性进行分割
      const [baseSaleAttrId, saleAttrName] = this.attrIdAndAttrName.split(":");
      // 向spu对象的spuSaleAttrList数组添加新的销售属性
      let newSaleAttr = {
        baseSaleAttrId,
        saleAttrName,
        spuSaleAttrValueList: [],
      };
      // 添加新的销售属性
      this.spu.spuSaleAttrList.push(newSaleAttr);
      // 清空选择框的数据
      this.attrIdAndAttrName = "";
    },
    // 表单保存按钮回调
    async addOrUpdateSpu() {
      //整理参数：需要整理照片墙的数据
      //携带参数：对于图片，需要携带imageName与imageUrl字段
      this.spu.spuImageList = this.spuImageList.map((item) => {
        return {
          imgName: item.name,
          imgUrl: (item.response && item.response.data) || item.url,
        };
      });

      //发请求
      let result = await this.$API.spu.reqAddOrUpdateSpu(this.spu);
      if (result.code == 200) {
        //提示
        this.$message({ type: "success", message: "保存成功" });
        //通知父组件回到场景0
        this.$emit("changeScene", 0);
      }
      //清除数据
      // Object.assign：es6中新增的方法，可以合并对象
      Object.assign(this._data, this.$options.data());
    },
    // 新增spu属性场景初始化spu数据
    async addSpuData(category3Id) {
       // 收集三级id
      this.spu.category3Id = category3Id;
      
      // 发送请求
      // 获取品牌数据
      let tradeMarkResult = await this.$API.spu.reqTrademarkList();
      // 获取平台中全部销售属性
      let baseSaleAttrResult = await this.$API.spu.reqBaseSaleAttrList();

      if (tradeMarkResult.code == 200) {
        // 存放数据
        this.tradeMarkList = tradeMarkResult.data;
      } else {
        this.$message({ type: "error", message: "获取品牌信息失败！" });
      }

      if (baseSaleAttrResult.code == 200) {
        // 存放数据
        this.saleAttrList = baseSaleAttrResult.data;
      } else {
        this.$message({ type: "error", message: "获取销售属性信息失败！" });
      }

     
    },
  },
  computed: {
    // 计算还未选择的销售属性
    unselectSaleAttr() {
      return this.saleAttrList.filter((item) => {
        return this.spu.spuSaleAttrList.every((item1) => {
          return item.name != item1.saleAttrName;
        });
      });
    },
  },
};
</script>

<style>
.el-tag + .el-tag {
  margin-left: 10px;
}
.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>