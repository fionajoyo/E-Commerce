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
        type: "category",
      },
      yAxis: {
        //   隐藏y轴
        show: false,
      },
      // 系列
      series: [
        {
          type: "line",
          data: [10, 7, 33, 12, 88, 9],
          smooth: true,
          //   拐点的样式设置
          itemStyle: {
            opacity: 0,
          },
          //   线条样式设置
          lineStyle: {
            color: "purple",
          },
          //   区域填充颜色
          areaStyle: {
            color: {
              type: "linear",
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                {
                  offset: 0,
                  color: "purple", // 0%处的颜色
                },
                {
                  offset: 1,
                  color: "#fff", // 100%处的颜色
                },
              ],
              global: false, // 缺省值为false
            },
          },
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