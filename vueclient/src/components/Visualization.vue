<template>
  <div id="main" style="width: 600px; height: 400px"></div>
  <div id="main2" style="width: 600px; height: 400px"></div>
  <div v-if="authenticated" class="content">
    <h2>Comments</h2>
    <ul class="mypost">
      <li v-for="(votes, key, _) in texts" :key="key">
        Group
        <div class="inline-bold">{{ key }}</div>
        <ul>
          <li v-for="(vote, _) in votes[0].aggregated" :key="key">
            {{ vote }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
import * as echarts from "echarts";
import { ref, computed, readonly } from "vue";
import { getAdminEntries } from "../api/api.js";
import * as constants from "../api/consts.js";

export default {
  setup: function () {
    const CHOICE_NUM = readonly(ref(constants.CHOICE_NUM));
    const TEXT = readonly(ref(constants.TEXT));
    const ORDER = readonly(constants.ORDER);
    const ORDER_MAP = readonly(constants.ORDER_MAP);
    const CHOICE_NUMS = readonly(constants.CHOICE_NUMS);

    const config = ref({
      headers: {
        Authorization: "",
      },
    });
    const token = ref("");
    const entries = ref([]);
    const authenticated = ref(false);

    const groupEntires = computed(() => {
      const result = entries.value.reduce((acc, cur) => {
        if (cur["type"] == CHOICE_NUM.value) {
          acc[cur.group_id] = acc[cur.group_id] || [];
          acc[cur.group_id].push({
            text: cur["text"],
            group_id: cur["group_id"],
            aggregated: cur["aggregated"],
          });
        }
        return acc;
      }, {});
      Object.keys(result).forEach((e) =>
        result[e].sort((a, b) => {
          return ORDER_MAP[a.text] - ORDER_MAP[b.text];
        })
      );
      // sort by key, though not needed here because data is populated in order, so retrieving via api is also ordered
      // moreover, here the keys are numeric value, and according to ES2015, the iteration order is ascending order for number-like keys
      const ordered = Object.keys(result)
        .sort()
        .reduce((obj, key) => {
          obj[key] = result[key];
          return obj;
        }, {});
      return ordered;
    });

    const texts = computed(() => {
      const result = entries.value.reduce(function (acc, cur) {
        if (cur["type"] == "text") {
          acc[cur.group_id] = acc[cur.group_id] || [];
          acc[cur.group_id].push({
            text: cur["text"],
            group_id: cur["group_id"],
            aggregated: cur["aggregated"],
          });
        }
        return acc;
      }, {});

      const groups = Object.keys(result).map((k) => `Group ${k}`);
      console.log(groups);
      const message = Object.entries(result).map((e) => e[1][0].aggregated);
      console.log(message);

      return result;
    });

    function transposeArray(array) {
      return array[0].map((_, columnIndex) =>
        array.map((row) => row[columnIndex])
      );
    }

    const chart = () => {
      const myChart = echarts.init(document.getElementById("main"));

      console.log(groupEntires);

      const groups = Object.keys(groupEntires.value).map((k) => `Group ${k}`);

      const xAxis = {
        type: "category",
        data: groups,
      };

      // destructure each key-value pair from the array, similar to pattern matching
      //   const content1 = Object.entries(groupEntires.value).map(([key, value]) =>
      //     value.map((entry) => entry.aggregated)
      //   );
      //   const content2 = transposeArray(content1);

      const xValueDict = Object.values(groupEntires.value)
        .flat()
        .reduce((result, item) => {
          // destructure objects
          const { text, aggregated } = item;
          return {
            ...result,
            [text]: [...(result[text] || []), aggregated],
          };
        }, {});

      //   const content = Object.entries(groupEntires.value).map(
      //     (e) => e[1][0].aggregated
      //   );
      //   const delivery = Object.entries(groupEntires.value).map(
      //     (e) => e[1][1].aggregated
      //   );
      //   const avg = Object.entries(groupEntires.value).map(
      //     (e) => (e[1][0].aggregated + e[1][1].aggregated) / 2
      //   );

      const series = Object.entries(xValueDict).map(([k, v]) => ({
        name: k,
        barGap: 0,
        data: v,
        type: "bar",
      }));

      const option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        legend: {
          data: CHOICE_NUMS,
        },
        xAxis: xAxis,
        yAxis: {
          type: "value",
        },
        series: series,
      };
      myChart.setOption(option);
    };

    const avgChart = () => {
      const myChart = echarts.init(document.getElementById("main2"));

      const groups = Object.keys(groupEntires.value).map((k) => `Group ${k}`);

      const xAxis = {
        type: "category",
        data: groups,
      };

      const avg = Object.entries(groupEntires.value).map(([key, value]) =>
        value
          .map((entry) => entry.aggregated)
          .reduce((acc, curr) => {
            if (curr == "NaN") {
              curr = 0;
            }
            return acc + curr;
          }, 0)
      );

      const option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        legend: {
          data: ["Average"],
        },
        xAxis: xAxis,
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "Average",
            barGap: 0,
            data: avg,
            type: "bar",
          },
        ],
      };
      myChart.setOption(option);
    };

    return {
      entries,
      groupEntires,
      token,
      config,
      texts,
      authenticated,
      chart,
      avgChart,
    };
  },
  methods: {
    async _load() {
      let response;
      try {
        response = await getAdminEntries(this.config);
        this.authenticated = true;
      } catch (e) {
        console.log(e);
        alert("You are not authroized to view this page.");
      }
      this.entries = response.data;
      this.chart();
      this.avgChart();
    },
  },
  created: function () {
    console.log("Hello!");
    this.token = localStorage.token;
    this.config["headers"]["Authorization"] = "token " + this.token;
  },
  mounted: function () {
    this._load();
  },
};
</script>

<style>
.inline-bold {
  display: inline-block;
  font-weight: bold;
}
</style>
