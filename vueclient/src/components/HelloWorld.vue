<template>
  <h1>BK Voting Form</h1>
  <br />
  {{ filterByGroupId }}
  <br />
  {{ scores }}
  <br />
  <div class="content">
    <el-tabs v-model="activeName0" class="demo-tabs" @tab-click="handleClick" tabPosition="left">
      <el-tab-pane v-for="(item, key, index0) in filterByGroupId" :key="index0" :label="'Group ' + key" :name="index0">
        <table>
          <tr>
            <th>Name</th>
            <th>NetID</th>
          </tr>
          <tr v-for="(student, index) in item" :key="index">
            <td>{{ student.name }}</td>
            <td>{{ student.net_id }}</td>
          </tr>
          <div>
            <input type="file" @change="uploadFile" />
            <button @click="submitFile(key)">Submit</button>
          </div>
        </table>
        <a :href="link[index0]">slides</a>
        <br />
        <!-- <a :href="link1">slides</a> -->
        <!-- <button @click="getLink">slides</button> -->
        <ul>
          <li>
            Content<br />
            <div class="radio-box">
              <input type="radio" name="content" value="1" v-model="scores[index0].content" id="delivery1" />
              <label for="TODO">1</label>
            </div>
            <div class="radio-box">
              <input type="radio" name="content" value="2" v-model="scores[index0].content" id="delivery2" />
              <label for="TODO">2</label>
            </div>
            <div class="radio-box">
              <input type="radio" name="content" value="3" v-model="scores[index0].content" id="delivery3" />
              <label for="TODO">3</label>
            </div>
            <div class="radio-box">
              <input type="radio" name="content" value="4" v-model="scores[index0].content" id="delivery4" />
              <label for="TODO">4</label>
            </div>
            <div class="radio-box">
              <input type="radio" name="content" value="5" v-model="scores[index0].content" id="delivery5" />
              <label for="TODO">5</label>
            </div>
          </li><br />

          <li>
            Delivery<br />
            <div class="radio-box">
              <input type="radio" name="delivery" value="1" v-model="scores[index0].delivery" id="delivery1" />
              <label for="TODO">1</label>
            </div>
            <div class="radio-box">
              <input type="radio" name="delivery" value="2" v-model="scores[index0].delivery" id="delivery2" />
              <label for="TODO">2</label>
            </div>
            <div class="radio-box">
              <input type="radio" name="delivery" value="3" v-model="scores[index0].delivery" id="delivery3" />
              <label for="TODO">3</label>
            </div>
            <div class="radio-box">
              <input type="radio" name="delivery" value="4" v-model="scores[index0].delivery" id="delivery4" />
              <label for="TODO">4</label>
            </div>
            <div class="radio-box">
              <input type="radio" name="delivery" value="5" v-model="scores[index0].delivery" id="delivery5" />
              <label for="TODO">5</label>
            </div>
          </li>
        </ul>
      </el-tab-pane>
    </el-tabs>
  </div>
  <!-- <button @click="print">Submit</button> -->
  <!-- <p>{{ fullName('your salut') }}</p> -->
  <!-- <a :href="fullName('your salut')">slides</a>
  <span>{{ fullName('Hi') }}</span> -->
  <a :href="link[index0]">slides</a>
  <br />
  <button class='blink' id="demo" @click="print">Click me to change my text color.</button>
  <a v-bind:href="'/job/' + a">aaa</a>
  {{ link }}
  <a :href="link[0]">slides</a>
  {{ link1 }}
  <footer>
    <h5>Luyao Wang. 2023.</h5>
  </footer>
  {{ movieName }}
  aaaa
  <!-- {{ links }} -->
</template>


<script setup>


</script>

<script>
import { getStudents, putGroupScore, postBook, postTask, postFile, postStudents, putFile, getFile } from '../api/api.js'
import { ref, computed, onMounted } from "vue";
// import { postFile, putGroupScore, postStudents, postBook, putFile, getFile } from '../api/api.js'
export default {
  setup() {



    const file = ref(null);
    const link = ref(['about:blank', 'about:blank', 'about:blank', 'about:blank']);
    const uploadFile = (event) => {
      file.value = event.target.files[0];
    };

    // function submitFile(id) {
    const submitFile = (id) => {
      var formdata = new FormData();
      formdata.append("file", file.value);
      formdata.append("id", id);

      postFile(formdata).then(response => {
        console.log(response)
        loadlinks()
        // console.log(response.response.status)
      }).catch(error => {
        console.log(`error: ${error} `)
        if (error.toString().includes("400")) {
          console.log("try again, now with put")
          putFile(formdata, id).then(res => loadlinks()
          )
        }
      });
      alert('Please refreash to update the newest link for the file you have just uploaded.')
    }

    const goToLink = () => {
      window.location.href = "http://stackoverflow.com";
    }

    const link1 = ref('')

    const links = computed(() => {
      var link0 = []
      for (var i = 0; i < 4; i++) {
        let locali = i
        getFile(i + 1).then(response => {
          console.log(response)
          link0[locali] = response.data.file
        })
      }
      console.log(link0)

      return link0
    })

    function loadlinks() {
      console.log(students.value)
      console.log(Object.keys(filterByGroupId))
      console.log(filterByGroupId)
      console.log(filterByGroupId.value)
      var len = Object.keys(filterByGroupId.value).length
      const x = 2
      console.log(len)
      for (var i = 0; i < len; i++) {
        let locali = i
        getFile(i + 1).then(response => {
          // console.log(x)
          console.log(locali)
          console.log(response)
          console.log(response.data.file)
          link.value[locali] = response.data.file
          console.log(link.value)

        })
      }
      console.log(link)
    }

    const scores = ref([{
      "content": 0,
      "delivery": 0
    },
    {
      "content": 0,
      "delivery": 0
    },
    {
      "content": 0,
      "delivery": 0
    },
    {
      "content": 0,
      "delivery": 0
    },
    {
      "content": 0,
      "delivery": 0
    },])


    function initScore() {
      var len = Object.keys(filterByGroupId.value).length

    }

    function handleClick1(id) {
      console.log("click")
      // console.log(`http://127.0.0.1:8000/api/file/${id}/`)
      window.location = getSlide(id)
      // window.location.href = ('https://careerkarma.com')
      console.log(window.location)
    }

    window.onpossiblyunhandledexception = function () {
      window.onerror.apply(this, arguments); // call
    }

    window.onerror = function (err) {
      console.log(err); // logs all errors
    }
    const students = ref([])

    const filterByGroupId = computed(() => {
      //https://stackoverflow.com/questions/40774697/how-can-i-group-an-array-of-objects-by-key
      var result = students.value.reduce(function (r, a) {
        r[a.group_id] = r[a.group_id] || [];
        r[a.group_id].push(a);
        return r;
      },
        Object.create(null))
      console.log(Object.entries(result))
      // return { "1": [{ "id": 1, "name": "Luyao Wang", "net_id": "lw337", "group_id": 1 }, { "id": 15, "name": "ll", "net_id": "lw", "group_id": 1 }], "2": [{ "id": 3, "name": "Sebastian Hou", "net_id": "lg666", "group_id": 2 }], "3": [{ "id": 2, "name": "Yijiu", "net_id": "yj666", "group_id": 3 }, { "id": 4, "name": "Shunfei Zhang", "net_id": "f8fq", "group_id": 3 }, { "id": 5, "name": "Qiang Zi", "net_id": "qz666", "group_id": 3 }, { "id": 6, "name": "Yijiu", "net_id": "yj666", "group_id": 3 }], "4": [{ "id": 7, "name": "Alice A", "net_id": "aa101", "group_id": 4 }, { "id": 8, "name": "Otto", "net_id": "otto7", "group_id": 4 }] }
      return result
    })

    const filterByGroupId1 = computed(() => {
      return { "1": [{ "id": 1, "name": "Luyao Wang", "net_id": "lw337", "group_id": 1 }, { "id": 15, "name": "ll", "net_id": "lw", "group_id": 1 }], "2": [{ "id": 3, "name": "Sebastian Hou", "net_id": "lg666", "group_id": 2 }], "3": [{ "id": 2, "name": "Yijiu", "net_id": "yj666", "group_id": 3 }, { "id": 4, "name": "Shunfei Zhang", "net_id": "f8fq", "group_id": 3 }, { "id": 5, "name": "Qiang Zi", "net_id": "qz666", "group_id": 3 }, { "id": 6, "name": "Yijiu", "net_id": "yj666", "group_id": 3 }], "4": [{ "id": 7, "name": "Alice A", "net_id": "aa101", "group_id": 4 }, { "id": 8, "name": "Otto", "net_id": "otto7", "group_id": 4 }] }
    })

    const cube = ref(1)

    const movieName = computed(() => { return { "1": [{ "id": 1, "name": "Luyao Wang", "net_id": "lw337", "group_id": 1 }, { "id": 15, "name": "ll", "net_id": "lw", "group_id": 1 }], "2": [{ "id": 3, "name": "Sebastian Hou", "net_id": "lg666", "group_id": 2 }], "3": [{ "id": 2, "name": "Yijiu", "net_id": "yj666", "group_id": 3 }, { "id": 4, "name": "Shunfei Zhang", "net_id": "f8fq", "group_id": 3 }, { "id": 5, "name": "Qiang Zi", "net_id": "qz666", "group_id": 3 }, { "id": 6, "name": "Yijiu", "net_id": "yj666", "group_id": 3 }], "4": [{ "id": 7, "name": "Alice A", "net_id": "aa101", "group_id": 4 }, { "id": 8, "name": "Otto", "net_id": "otto7", "group_id": 4 }] } })

    onMounted(() => {
      console.log(cube.value)
      console.log(filterByGroupId.value)
      // console.log(movieName.value)
    })

    return {
      file,
      uploadFile,
      submitFile,
      loadlinks,
      link,
      goToLink,
      filterByGroupId,
      students,
      link1,
      movieName,
      scores,
      links
    }
  },
  name: 'HelloWorld',
  data() {
    return {
      // file: ref(null),

      a: 'aaabbb',
      content: 0,
      delivery: 0,
      testData: [{ "id": 1, "name": "Luyao Wang", "net_id": "lw337", "group_id": 1 }, { "id": 3, "name": "Fname2 Fname2", "net_id": "ni002", "group_id": 1 }],
      listData: { "Group 1": 1, "Group 2": 2, "Group 3": 3, "Group 4": 4 },
      activeName0: 0,
      activeName1: "tab1",
      msg: 'Welcome to Your Vue.js App',
    }
  },
  computed: {
    fullName: (app) => (salut) => {
      return salut + ' ' + app.firstName + ' ' + app.lastName
    },
    getLink: { get(id) { return this.getSlide(id) } },
    score() {
      return {
        "content": this.content,      // return Promise.resolve("Success");

        "delivery": this.delivery
      }
    },
    // filterByGroupId() {
    //   //https://stackoverflow.com/questions/40774697/how-can-i-group-an-array-of-objects-by-key
    //   var result = this.students.reduce(function (r, a) {
    //     r[a.group_id] = r[a.group_id] || [];
    //     r[a.group_id].push(a);
    //     return r;
    //   }, Object.create(null));
    //   return result
    // },
  },
  methods: {
    // uploadFile(event) {
    //   console.log(1)
    //   this.file.value = event.target.files[0];
    //   console.log(event)
    // },
    ForcesUpdateComponent() {
      // our code
      this.$forceUpdate();  // Notice we have to use a $ here
      // our code
    },
    print() {
      this.a = "aaaccc" + new Date()
      this.loadlinks()
      // console.log(new Date())
      // console.log(this.getSlide(1))
      // console.log(this.link)
      // console.log(this.students)
      // console.log(this.filterByGroupId)
    },
    get1() { return 1 },
    isSelected(id) {
      return true;
    },
    // fullName(salut) {
    //   return `${salut} ${this.firstName} ${this.lastName}`
    // },

    loadStudents() {
      getStudents().then(response => {
        this.students = response.data
        this.loadlinks()
      })
      // return Promise.resolve("Success");
    },
    changeScore() {
      putGroupScore(1, 1000).then(response => {
        console.log(response)
        this.loadStudents()
      })
    },
    submit(id) {
      var formdata = new FormData();
      formdata.append("file", this.file.value);
      formdata.append("id", id);

      this.postFile(formdata).then(response => {
        console.log(response)
        // console.log(response.response.status)
      }).catch(error => {
        console.log(`error: ${error} `)
        if (error.toString().includes("400")) {
          console.log("try again, now with put")
          putFile(formdata, id)
        }

      });
      // this.loadlinks()
    },
    submitFile1() {
      // putGroupScore(1, 1000)
      // postTask()
      // postStudents()
      // getStudents().then(response => {
      //   console.log(response)
      // })
      postBook('l', '1').then(response => {
        console.log(response)
      })
    },
    getSlide(id) {
      // window.location = 'http://www.google.com';
      getFile(id).then(response => {
        console.log(response)
        console.log(response.data.file)
        return response.data.file
      })

    }
  },
  created: function () {
    this.loadStudents()
    // .then(Response => this.loadlinks())
    // setTimeout(() => { this.loadlinks() }, 1000);

    // this.loadlinks()

    // console.log(Object.keys(this.filterByGroupId))
    // console.log(this.filterByGroupId)

  },
  mounted() {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #a6642e;
}

table {
  display: table;
  border-collapse: separate;
  border-spacing: 5px;
  border-color: gray;
}

.content {
  max-width: 500px;
  margin: auto;
  background: white;
  padding: 10px;
}


form {
  width: 100%;
}

input {
  /* width: 20px; */
  display: block;
  margin: 0px auto;
}

div.radio-box {
  width: 30px;
  display: inline-block;
  /* margin: 5px;
  background-color: yellow; */
}

.radio-box label {
  display: block;
  /* width: 30px; */
  text-align: center;
}

.radio-box input {
  /* width: 20px; */
  display: block;
  /* margin: 0px auto; */
}

.blink {
  background: none;
  border: none;
  color: blue;
}

.blink:hover {
  color: rgb(0, 136, 255);
  transition: 0.7s;
}

.blink:active {
  color: rgb(23, 0, 93);
  transition: 0.7s;
}
</style>
