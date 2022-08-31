<template>
  <div>
    <!-- 三级联动 -->
    <el-card style="margin: 20px 0">
      <categorySelect
        @getCategoryId="getCategoryId"
        :show="!isShowTable"
      ></categorySelect>
    </el-card>
    <!-- 数据表格 -->
    <el-card>
      <!-- 表格 -->
      <div v-show="isShowTable">
        <el-button
          type="primary"
          icon="el-icon-plus"
          :disabled="attrList.length === 0"
          @click="addAttr"
          >
          添加属性
          </el-button>
          
        <!-- 表格，展示平台属性 -->
        <el-table :data="attrList" style="width: 100%" border>
          <el-table-column type="index" label="序号" width="80" align="center">
          </el-table-column>
          <el-table-column prop="attrName" label="属性名称" width="150">
          </el-table-column>
          <el-table-column prop="prop" label="属性值列表" width="width">
            <template slot-scope="{ row, $index }">
              <el-tag
                type="success"
                v-for="(attrValue, index) in row.attrValueList"
                :key="attrValue.id"
                style="margin: 5px 20px"
              >
                {{ attrValue.valueName }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="prop" label="操作" width="150">
            <template slot-scope="{ row, $index }">
              <!-- 修改按钮 -->
              <el-button
                type="warning"
                icon="el-icon-edit"
                size="mini"
                @click="updateAttr(row)"
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
      </div>
      <!-- 修改|新增 -->
      <div v-show="!isShowTable">
        <el-form :inline="true" ref="form" label-width="80px" :model="attrInfo">
          <el-form-item label="属性名">
            <el-input
              placeholder="请输入属性名"
              v-model="attrInfo.attrName"
            ></el-input>
          </el-form-item>
        </el-form>

        <el-button
          type="primary"
          icon="el-icon-plus"
          @click="addAttrValue"
          :disabled="!attrInfo.attrName"
          >添加属性值</el-button
        >
        <el-button @click="isShowTable = true">取消</el-button>

        <el-table
          style="width: 100%; margin: 20px 0"
          border
          :data="attrInfo.attrValueList"
        >
          <el-table-column type="index" label="序号" width="80" align="center">
          </el-table-column>
          <el-table-column prop="prop" label="属性值名称" width="width">
            <template slot-scope="{ row, $index }">
              <el-input
                v-model="row.valueName"
                placeholder="请输入属性值名称"
                size="mini"
                v-if="row.flag"
                @blur="toLook(row)"
                @keyup.native.enter="toLook(row)"
                :ref="$index"
              ></el-input>
              <span v-else @click="toEdit(row, $index)" style="display: block">
                {{ row.valueName }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="prop" label="操作" width="width">
            <!-- 气泡删除确认框 -->
            <template slot-scope="{ row, $index }">
              <el-popconfirm
                :title="`确定删除${row.valueName}吗？`"
                @onConfirm="deleteAttrValue($index)"
              >
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  slot="reference"
                ></el-button>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>

        <el-button
          type="primary"
          :disabled="attrInfo.attrValueList.length < 1"
          @click="addOrUpdateAttr"
        >
          保存
        </el-button>
        <el-button @click="isShowTable = true">取消</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
// 按需引入lodash当中的深拷贝
import cloneDeep from "lodash/cloneDeep";

export default {
  name: "attr",
  data() {
    return {
      // 菜单一级id
      category1Id: "",
      // 菜单二级id
      category2Id: "",
      // 菜单三级id
      category3Id: "",
      // 平台属性
      attrList: [],
      // 是否展示表格
      isShowTable: true,
      // 收集新增|修改属性使用
      attrInfo: {
        // 属性名
        attrName: "",
        // 属性值
        attrValueList: [],
        categoryId: 0,
        categoryLevel: 3,
      },
    };
  },
  methods: {
    // 自定义事件回调，获取三级联动组件选择的id
    getCategoryId({ category1Id, category2Id, category3Id }) {
      // 如果category3Id不为空，则可以向服务器发送请求获取平台属性列表数据
      if (category3Id) {
        this.category1Id = category1Id;
        this.category2Id = category2Id;
        this.category3Id = category3Id;
        // 清除原有的平台属性列表数据
        this.attrList = [];
        // 发送请求
        this.getAttrList();
      } else {
        // 清空已有的平台属性列表数据
        this.attrList = [];
      }
    },
    // 获取平台属性列表数据
    async getAttrList() {
      const { category1Id, category2Id, category3Id } = this;
      let result = await this.$API.attr.reqAttrList(
        category1Id,
        category2Id,
        category3Id
      );
      if (result.code === 200) {
        this.attrList = result.data;
      }
    },
    // 添加属性值回调（新增界面）
    addAttrValue() {
      // 向属性值数组添加元素
      // attrId：添加属性的id
      // valueName：属性值的名称
      this.attrInfo.attrValueList.push({
        attrId: this.attrInfo.id,
        valueName: "",
        flag: true,
      });
      // 自动聚焦最后一项（新增的
      this.$nextTick(() => {
        //获取相应的input表单元素实现聚焦
        this.$refs[this.attrInfo.attrValueList.length - 1].focus();
      });
    },
    // 添加属性按钮回调（表格界面）
    addAttr() {
      // 切换table
      this.isShowTable = false;
      // 清除收集新增|修改属性
      this.attrInfo = {
        // 属性名
        attrName: "",
        // 属性值
        attrValueList: [],
        categoryId: this.category3Id,
        categoryLevel: 3,
      };
    },
    // 修改属性按钮回调
    updateAttr(row) {
      // 切换table
      this.isShowTable = false;
      // 深拷贝（数据结构复杂，需要使用深拷贝解决）
      this.attrInfo = cloneDeep(row);
      //在修改某一个属性的时候，将相应的属性值元素添加上flag这个标记
      this.attrInfo.attrValueList.forEach((item) => {
        //这样书写也可以给属性值添加flag自动，但是会发现视图不会跟着变化（因为flag不是响应式数据）
        //因为Vue无法探测普通的新增 property,这样书写的属性并非响应式属性（数据变化视图跟这边）
        //第一个参数:对象  第二个参数:添加新的响应式属性  第三参数：新的属性的属性值
        this.$set(item, "flag", false);
      });
    },
    // 输入框失焦事件
    toLook(row) {
      // 校验输入框输入，输入为空时不可保存
      if (row.valueName.trim() == "") {
        // 可以删除该项
        this.$message("请输入合理值！");
        return;
      }
      // 新增属性值不可重复
      if (
        this.attrInfo.attrValueList.some((item) => {
          // 去除row
          if (row !== item) {
            return row.valueName == item.valueName;
          }
        })
      ) {
        this.$message("请不要输入重复值！");
        return;
      }

      row.flag = false;
    },
    //点击span的回调，变为编辑模式
    toEdit(row, index) {
      row.flag = true;
      //获取input节点，实现自动聚焦
      //需要注意：点击span的时候，切换为input变为编辑模式，但是需要注意，对于浏览器而言，页面重绘与重拍耗时间的
      //点击span的时候，重绘重拍一个input它是需要耗费事件，因此我们不可能一点击span立马获取到input
      //$nextTick,当节点渲染完毕了，会执行一次
      this.$nextTick(() => {
        //获取相应的input表单元素实现聚焦
        this.$refs[index].focus();
      });
    },
    // 气泡删除确认框
    deleteAttrValue(index) {
      // 删除属性值
      this.attrInfo.attrValueList.splice(index, 1);
    },
    // 保存按钮，进行添加属性或者修改属性
    async addOrUpdateAttr() {
      // 整理参数，删除空的属性值并删除属性中的flag值
      this.attrInfo.attrValueList = this.attrInfo.attrValueList.filter(
        (item) => {
          // 过滤掉属性值不为空的
          if (item.valueName != "") {
            // 删除掉flag
            delete item.flag;
            return true;
          }
        }
      );
      if (this.attrInfo.attrValueList.length < 1) {
        // 无属性了
        this.$message({ type: "warning", message: "不可上传空属性值！" });
        return;
      }
      try {
        await this.$API.attr.reqAddOrUpdateAttr(this.attrInfo);
        this.$message({ type: "success", message: "保存成功" });
        // 重新获取最新数据
        this.isShowTable = true;
        this.getAttrList();
      } catch (error) {
        this.$message.error(error.message);
      }
    },
  },
};
</script>

<style>
</style>