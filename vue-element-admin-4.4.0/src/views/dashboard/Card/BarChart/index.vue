<template>
  <div class="charts" ref="charts"></div>
</template>

<script>
// 引入echarts
import echarts from "echarts";
export default {
  name: "LineCharts",
  mounted() {
    //   初始化echarts实例
    let lineCharts = echarts.init(this.$refs.charts);
    // 配置数据
    lineCharts.setOption({
      xAxis: {
        //   隐藏x轴
        show: false,
        // 均分
        type: "category",
      },
      yAxis: {
        //   隐藏y轴
        show: false,
      },
      // 系列
      series: [
        {
          type: "bar",
          data: [10, 7, 33, 12, 88, 9,33,22,8],
          color:'cyan',
        },
      ],
      // 布局调试
      grid: {
        left: 0,
        top: 0,
        right: 0,
        bottom: 5,
      },
    });
  },
};
</script>

<style>
.charts {
  width: 100%;
  height: 100%;
}
</style>