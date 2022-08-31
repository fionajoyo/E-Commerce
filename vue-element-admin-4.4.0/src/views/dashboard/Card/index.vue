<template>
  <div>
    <!-- 四个卡片 -->
    <el-row :gutter="10">
      <el-col :span="6">
        <el-card>
          <Detail title="总销售额" count="￥126560">
            <template slot="charts">
              <div style="padding-top: 5%">
                <span>
                  周同比&nbsp;56.67%
                  <i class="el-icon-top"></i>
                </span>
                &nbsp;
                <span>
                  日同比&nbsp;19.96%
                  <i class="el-icon-bottom"></i>
                </span>
              </div>
            </template>
            <template slot="footer">
              <div>
                <span>日销售额 ￥12423</span>
              </div>
            </template>
          </Detail>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <Detail title="访问量" count="88460">
            <template slot="charts">
              <LineChart></LineChart>
            </template>
            <template slot="footer">
              <div>
                <span>日访问量 1234</span>
              </div>
            </template>
          </Detail>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <Detail title="支付笔数" count="88460">
            <template slot="charts">
              <BarChart></BarChart>
            </template>
            <template slot="footer">
              <div>
                <span>转化率 65%</span>
              </div>
            </template>
          </Detail>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <Detail title="运营活动效果" count="78%">
            <template slot="charts">
              <ProgressChart></ProgressChart>
            </template>
            <template slot="footer">
              <div>
                <span>
                  周同比&nbsp;56.67%
                  <i class="el-icon-top"></i>
                </span>
                &nbsp;
                <span>
                  日同比&nbsp;19.96%
                  <i class="el-icon-bottom"></i>
                </span>
              </div>
            </template>
          </Detail>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Detail from "./Detail";
import LineChart from "./LineChart";
import BarChart from "./BarChart";
import ProgressChart from "./ProgressChart";
export default {
  name: "Card",
  components: {
    Detail,
    LineChart,
    BarChart,
    ProgressChart,
  },
};
</script>

<style>
</style>