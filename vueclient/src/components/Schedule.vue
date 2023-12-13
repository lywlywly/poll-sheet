<template>
  <table>
    <tr>
      <th>Week</th>
      <th>Date</th>
      <th>Reading</th>
      <th>Lecture</th>
      <th>Lab</th>
      <th>Assignments</th>
    </tr>


    <tr>
      <td rowspan="4">1</td>
      <td>Mon 8/21</td>
      <td>50</td>
      <td>Introduction</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <!-- <td>2</td> -->
      <td>Tue 8/22</td>
      <td>94</td>
      <td>Hello World, Java!</td>
      <td>Setting Up Your Computer</td>
      <td><router-link to="/helloworld">HelloWorld</router-link> <a></a></td>
    </tr>
    <tr>
      <td>Wed 8/23</td>
      <td>94</td>
      <td>Hello World, Java!</td>
      <td>Setting Up Your Computer</td>
      <td>HelloWorld</td>
    </tr>
    <tr>
      <td>Thu 8/24</td>
      <td>94</td>
      <td>Hello World, Java!</td>
      <td>Setting Up Your Computer</td>
      <td>HelloWorld</td>
    </tr>


    <tr>
      <td rowspan="4">2</td>
      <td>Mon 8/21</td>
      <td>50</td>
      <td>Introduction</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <!-- <td>2</td> -->
      <td>Tue 8/22</td>
      <td>94</td>
      <td>Hello World, Java!</td>
      <td>Setting Up Your Computer</td>
      <td>HelloWorld</td>
    </tr>
    <tr>
      <td>Wed 8/23</td>
      <td>94</td>
      <td>Hello World, Java!</td>
      <td>Setting Up Your Computer</td>
      <td>HelloWorld</td>
    </tr>
    <tr>
      <td>Thu 8/24</td>
      <td>94</td>
      <td>Hello World, Java!</td>
      <td>Setting Up Your Computer</td>
      <td>HelloWorld</td>
    </tr>
  </table>

</template>

<script>
import { login } from '../api/api.js'
import { marked } from 'marked';
export default {
  //   name: 'App',
  data() {
    return {
      markdown: "# Hello World",
    };
  },
  computed: {
    markdownToHtml() {
      return marked(this.markdown);
    }
  },
  methods: {
  }
}
</script>

<style scoped>
table,
th,
td {
  border: 1px solid black;
  border-collapse: collapse;
  padding: 7px;
}

tr:nth-child(even) {
  background-color: rgba(150, 212, 212, 0.4);
}

th:nth-child(even),
td:nth-child(even) {
  background-color: rgba(150, 212, 212, 0.4);
}

/* th {
    background-color: rgba(57, 85, 85, 0.4);
} */
</style>