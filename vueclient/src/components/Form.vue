<template>
  <h1>Voting Form</h1>
  <h3 v-if="!loggedIn">You are not logged in</h3>
  <div v-if="loggedIn">
    Name:
    <div class="inline-bold">{{ loginInfo.username }}</div>
  </div>
  <div v-if="loggedIn">
    Group:
    <div class="inline-bold">{{ loginInfo.status ?? loginInfo.group }}</div>
  </div>

  <div class="login">
    <!-- the submit event will no longer reload the page -->
    <!-- https://vuejs.org/guide/essentials/event-handling.html#event-modifiers -->
    <form
      @submit.prevent="submitLoginForm()"
      class="form-example"
      ref="loginForm"
    >
      <table class="login-table">
        <tr>
          <td align="right">Email:</td>
          <td align="left">
            <input
              type="text"
              name="email"
              placeholder="email"
              autocomplete="email"
              id="email"
              v-model="email"
              required
            />
          </td>
        </tr>
        <tr>
          <td align="right">Password:</td>
          <td align="left">
            <input
              type="password"
              name="password"
              placeholder="password"
              autocomplete="current-password"
              id="password"
              v-model="password"
              required
            />
          </td>
        </tr>
      </table>

      <div class="submit-button">
        <input type="submit" value="Login" />
        <button @click="logout()">logout</button>
      </div>
    </form>
  </div>

  <h2>Your vote</h2>
  <h3 v-if="Object.keys(groupedMyCurrentVotes).length == 0">
    You haven't voted yet.
  </h3>
  <ul class="mypost">
    <li v-for="(votes, key, _) in groupedMyCurrentVotes" :key="key">
      Group
      <div class="inline-bold">{{ key }}</div>
      <ul>
        <li v-for="(vote, _) in votes" :key="key">
          {{ vote.entry }}:
          <div v-if="vote.type === CHOICE_NUM" class="inline-bold">
            {{ vote.choice }}
          </div>
          <div v-if="vote.type === TEXT" class="inline-bold">
            {{ vote.content }}
          </div>
        </li>
      </ul>
    </li>
  </ul>

  <h3 v-if="!loggedIn" class="center-text">Sign in to vote</h3>
  <div class="content">
    <el-tabs v-model="activeName0" class="demo-tabs" tabPosition="left">
      <el-tab-pane
        v-for="(entries, key, index0) in groupedEntires"
        :key="index0"
        :label="'Group ' + key"
        :name="index0"
      >
        <table class="group">
          <tr>
            <th>Name</th>
            <th>NetID</th>
          </tr>
          <tr v-for="(student, index) in groupedStudents[key]" :key="index">
            <td>{{ student.name }}</td>
            <td>{{ student.net_id }}</td>
          </tr>
        </table>

        <!-- <div class="files">
          <input type="file" @change="uploadFile" /><br />
          <button @click="submitFile(key)">Submit</button>
          <a :href="links[index0]">slides</a>
        </div> -->
        <ul class="post">
          <li v-for="(entry, index) in entries" :key="key">
            {{ entry.text }}<br />
            <div class="entry" v-if="entry.type === CHOICE_NUM">
              <ul class="ul-score">
                <li
                  v-for="(choice, _) in choices.filter(
                    (c) => c.poll == entry.id
                  )"
                  :key="key"
                  class="li-score"
                >
                  <div class="radio-box">
                    <input
                      type="radio"
                      :name="index0.toString() + index.toString()"
                      :value="choice.choice_text"
                      v-model="updatedGroupedEntries[index0 + 1][index].score"
                      id="delivery1"
                      :disabled="key == loginInfo.group"
                    />
                    <label for="TODO">{{ choice.choice_text }}</label>
                  </div>
                </li>
              </ul>
            </div>
            <div class="entry" v-if="entry.type === TEXT">
              <textarea
                class="vote-text"
                v-model="updatedGroupedEntries[index0 + 1][index].content"
                :disabled="key == loginInfo.group"
              ></textarea>
            </div>
          </li>
        </ul>
      </el-tab-pane>
    </el-tabs>
  </div>
  <div class="submit-button">
    <!-- <button @click="preview">Preview</button> -->
    <button v-if="loggedIn" @click="postVotes">Submit</button>
  </div>
  <footer></footer>
</template>

<script setup></script>

<script>
import {
  getStudents,
  postFile,
  putFile,
  getFile,
  login,
  getEntries,
  getChoices,
  postVote,
  getCurrentUserInfo,
  getVote,
  deleteVote,
} from "../api/api.js";
import * as constants from "../api/consts.js";
import { ref, computed, readonly, reactive } from "vue";
export default {
  setup: function () {
    // constants
    const CHOICE_NUM = readonly(ref(constants.CHOICE_NUM));
    const TEXT = readonly(ref(constants.TEXT));
    const ORDER = readonly(constants.ORDER);
    const ORDER_MAP = readonly(constants.ORDER_MAP);

    const token = ref("");
    const loggedIn = ref(false);
    const activeName0 = ref(0);
    const email = ref("");
    const password = ref("");
    const loginInfo = ref("");
    const file = ref(null);
    const links = ref([
      "about:blank",
      "about:blank",
      "about:blank",
      "about:blank",
    ]);
    const students = ref([]);
    const entries = ref([]);
    const choices = ref([]);
    const updatedGroupedEntries = ref({});

    const uploadFile = (event) => {
      file.value = event.target.files[0];
    };
    const submitFile = (id) => {
      const formdata = new FormData();
      formdata.append("file", file.value);
      formdata.append("id", id);

      postFile(formdata, config.value)
        .then((response) => {
          console.log(response);
          loadlinks();
        })
        .catch((error) => {
          console.log(`error: ${error} `);
          if (error.toString().includes("400")) {
            console.log("try again, now with put");
            putFile(formdata, id, config.value).then((res) => loadlinks());
          }
        });
      alert(
        "Please refresh to update the newest links for the file you have just uploaded."
      );
    };

    const findChoiceId = (e, v) => (x) =>
      x["poll"] == e && x["choice_text"] == v;

    function loadlinks() {
      const len = Object.keys(groupedStudents.value).length;
      for (let i = 0; i < len; i++) {
        let locali = i;
        getFile(i + 1, config.value).then((response) => {
          links.value[locali] = response.data.file;
        });
      }
    }

    // window.onpossiblyunhandledexception = function () {
    //   window.onerror.apply(this, arguments); // call
    // }

    // window.onerror = function (err) {
    //   console.log(err); // logs all errors
    // }

    const loadMyVote = async () => {
      const response = await getVote(config.value);
      myCurrentVote.value = response.data;
    };

    const postVotes = async () => {
      for (let i in myCurrentVotePks.value) {
        await deleteVote(myCurrentVotePks.value[i], config.value);
      }
      for (let i in postVotePayload.value) {
        postVote(postVotePayload.value[i], config.value);
      }
      // loadMyVote()
      // retrieving directly after post can cause missing data because of DB delay
      alert("refresh to reload your votes");
    };

    const postVotePayload = computed(() => {
      const post = [];
      for (let i in updatedGroupedEntries.value) {
        for (let j = 0; j < updatedGroupedEntries.value[i].length; j++) {
          if (updatedGroupedEntries.value[i][j]["type"] == CHOICE_NUM.value) {
            const rawScore = updatedGroupedEntries.value[i][j]["score"];
            const choiceText = rawScore > 0 ? rawScore : 1;
            const pollId = updatedGroupedEntries.value[i][j]["id"];
            const choiceId = choices.value.filter(
              findChoiceId(pollId, choiceText)
            )[0]["id"];
            post.push({
              entry: pollId,
              choice: choiceId,
            });
          } else if (updatedGroupedEntries.value[i][j]["type"] == TEXT.value) {
            var choiceId = choices.value.filter(
              findChoiceId(
                updatedGroupedEntries.value[i][j]["id"],
                "Enter your words"
              )
            )[0]["id"];
            post.push({
              entry: updatedGroupedEntries.value[i][j]["id"],
              choice: choiceId,
              content: updatedGroupedEntries.value[i][j]["content"],
            });
          }
        }
      }
      return post;
    });

    // { "1": [ { "id": 7, "name": "student7", "net_id": "007", "user": 7, "group_id": 1 }, { "id": 8, "name": "student8", "net_id": "008", "user": 8, "group_id": 1 } ], ... }
    const groupedStudents = computed(() => {
      //https://stackoverflow.com/questions/40774697/how-can-i-group-an-array-of-objects-by-key
      const result = students.value.reduce((r, a) => {
        r[a.group_id] = r[a.group_id] || [];
        r[a.group_id].push(a);
        return r;
      }, Object.create(null));
      return result;
    });

    const groupedEntires = computed(() => {
      const result = entries.value.reduce(function (r, a) {
        r[a.group_id] = r[a.group_id] || [];
        r[a.group_id].push({
          id: a["id"],
          text: a["text"],
          group_id: a["group_id"],
          score: 0,
          type: a["type"],
          content: "enter your comments here",
        });
        return r;
      }, Object.create(null));

      const myOrder = (a, b) => {
        return ORDER.indexOf(a.text) - ORDER.indexOf(b.text);
      };
      const sortedData = Object.fromEntries(
        Object.entries(result).map(([key, entries]) => [
          key,
          entries.sort(myOrder),
        ])
      );

      console.log(sortedData);
      return sortedData;
    });

    const myCurrentVote = ref([]);

    function getSafe(fn, defaultVal) {
      try {
        return fn();
      } catch (e) {
        return defaultVal;
      }
    }

    function entryIdByChoiceId(choiceId) {
      return choices.value.filter((c) => c.id == choiceId)[0].poll;
    }

    const groupedMyCurrentVotes = computed(() => {
      if (!loggedIn.value) return {};
      const result_0 = myCurrentVote.value.map((m) => ({
        group_id: getSafe(
          () =>
            entries.value.filter((e) => e.id == entryIdByChoiceId(m.choice))[0]
              .group_id
        ),
        entry: getSafe(
          () =>
            entries.value.filter((e) => e.id == entryIdByChoiceId(m.choice))[0]
              .text
        ),
        type: getSafe(
          () =>
            entries.value.filter((e) => e.id == entryIdByChoiceId(m.choice))[0]
              .type
        ),
        id: m.id,
        choice: getSafe(
          () => choices.value.filter((c) => c.id == m.choice)[0].choice_text
        ),
        content: m.content,
      }));
      const result = result_0.reduce(function (r, a) {
        r[a.group_id] = r[a.group_id] || [];
        r[a.group_id].push({
          entry: a["entry"],
          type: a["type"],
          group_id: a["group_id"],
          choice: a["choice"],
          content: a["content"],
        });
        return r;
      }, Object.create(null));
      // reorder to ["Content", "Delivery", "Any other words"]
      Object.keys(result).forEach((e) =>
        result[e].sort((a, b) => {
          return ORDER_MAP[a.entry] - ORDER_MAP[b.entry];
        })
      );

      return result;
    });

    const myCurrentVotePks = computed(() => {
      console.log(myCurrentVote.value);
      const result = myCurrentVote.value.map((m) => m.id);
      return result;
    });

    const config = ref({
      headers: {
        Authorization: "",
      },
    });

    return {
      config,
      activeName0,
      email,
      password,
      loginInfo,
      file,
      links,
      groupedStudents,
      students,
      entries,
      groupedEntires,
      choices,
      updatedGroupedEntries,
      // postVotePayload,
      groupedMyCurrentVotes,
      token,
      loggedIn,
      myCurrentVotePks,
      myCurrentVote,
      CHOICE_NUM,
      TEXT,
      ORDER,
      loadMyVote,
      uploadFile,
      submitFile,
      loadlinks,
      postVotes,
      findChoiceId,
    };
  },

  data() {
    return {};
  },

  methods: {
    async submitLoginForm() {
      let response;
      try {
        response = await login(this.email, this.password);
      } catch (e) {
        alert(JSON.stringify(e.response.data));
        this.logout();
      }
      this.token = response.data.key;
      localStorage.token = this.token;
      this.config.headers.Authorization = "token " + this.token;
      this._load();
      this.resetLoginForm();
    },

    preview() {},

    resetLoginForm() {
      this.$refs.loginForm.reset();
      this.email = "";
      this.password = "";
    },

    logout() {
      localStorage.clear();
      this.config = "";
      this.token = "";
      location.reload();
    },

    async _load() {
      this.loginInfo = (await getCurrentUserInfo(this.config)).data;
      this.loggedIn = true;
      const responses = await Promise.all([
        getChoices(this.config),
        getEntries(this.config),
        getStudents(this.config),
      ]);
      this.choices = responses[0].data;
      this.entries = responses[1].data;
      this.students = responses[2].data;
      this.updatedGroupedEntries = this.groupedEntires;
      // this.loadlinks()
      this.loadMyVote();
    },

    submitFile(id) {
      const formdata = new FormData();
      formdata.append("file", this.file.value);
      formdata.append("id", id);
      this.postFile(formdata)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(`error: ${error} `);
          if (error.toString().includes("400")) {
            console.log("try again, now with put");
            putFile(formdata, id);
          }
        });
    },
  },

  created: function () {
    console.log("Hello!");
    this.token = localStorage.token;
    this.config["headers"]["Authorization"] = "token " + this.token;
    this._load();
  },

  mounted: function () {},

  beforeUnmount: function () {
    console.log("Bye!");
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* min css */

div.login {
  max-width: 300px;
  /* margin: auto; */
  padding: 10px;
}

.login-table {
  margin-left: auto;
  margin-right: auto;
  border: 1px solid;
}

table.group {
  margin-left: 10px;
  display: table;
  border-collapse: collapse;
  /* padding: 50px; */
  /* border-spacing: 8px; */
  text-align: left;
}

table.group th {
  padding-top: 6px;
  padding-bottom: 6px;
  text-align: left;
  background-color: #04aa6d;
  color: white;
}

table.group td,
table.group th {
  border: 1px solid #ddd;
  padding: 8px;
}

table.group tr:nth-child(even) {
  background-color: #f2f2f2;
}

.login-table input {
  width: 200px;
}

button {
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 5px;
  margin-bottom: 5px;
}

.submit-button {
  /* for inside a <div> */
  text-align: center;

  /* margin: 0 auto;
  display: block; */

  /* use flexbox */
  /* display: flex;
  align-items: center;
  justify-content: center; */

  /* border: 1px solid */
}

.inline-bold {
  display: inline-block;
  font-weight: bold;
}

.content {
  max-width: 600px;
  margin: auto;
  background: white;
  padding: 10px;
}

.center-text {
  text-align: center;
}

div.files {
  /* margin: 5px; */
  text-align: start;
}

div.files input {
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 5px;
  margin-bottom: 5px;
}

div.radio-box {
  width: 30px;
  display: inline-block;
}

.radio-box label {
  display: block;
  text-align: center;
}

.radio-box input {
  display: block;
  margin: 0px auto;
}

ul {
  /* list-style-type: none;
  padding: 0; */
  /* margin: 110px; */
  margin: 10px 0;
  /* padding-inline-start: 20px; */
}

.ul-score {
  list-style-type: none;
}

.li-score {
  display: inline-block;
}

.vote-text {
  margin-top: 10px;
  resize: none;
  width: 350px;
  height: 100px;
}

/* li {} */

/* min css */
</style>
