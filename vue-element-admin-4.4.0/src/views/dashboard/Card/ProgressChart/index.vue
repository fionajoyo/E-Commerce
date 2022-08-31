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
        // 设置最小值/最大值
        min: 0,
        max: 100,
      },
      yAxis: {
        //   隐藏y轴
        show: false,
        // 均分
        type: "category",
      },
      // 系列
      series: [
        {
          type: "bar",
          data: [78],
          color: "yellowgreen",
          // 设置柱状图宽度
          barWidth: 13,
          // 设置背景颜色
          showBackground: true,
          backgroundStyle: {
            color: "#eee",
          },
          // 文本设置
          label: {
            show: true,
            formatter: "|",
            position: "right",
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