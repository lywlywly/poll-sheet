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
            <th>NetId</th>
          </tr>
          <tr v-for="(student, index) in groupedStudents[key]" :key="index">
            <td>{{ student.name }}</td>
            <td>{{ student.net_id }}</td>
          </tr>
        </table>

        <EditDialog
          :dialogVisible="dialogVisible"
          :original-text="groupTexts[key - 1]"
          @confirmDialog="setGroupText($event, key)"
          @cancelDialog="dialogVisible = false"
        ></EditDialog>

        <h3>Group introduction</h3>

        <div v-html="md2Html(groupTexts[key - 1])" class="group_text"></div>

        <el-button
          text
          @click="dialogVisible = true"
          v-if="loginInfo.group == key"
        >
          Edit Introduction
        </el-button>

        <!-- TODO -->
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
    <button @click="preview">Preview</button>
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
  getGroups,
  postGroupText,
} from "../api/api.js";
import * as constants from "../api/consts.js";
import { ref, computed, readonly, reactive } from "vue";
import EditDialog from "./EditDialog.vue";
import { marked } from "marked";
export default {
  components: {
    EditDialog,
  },
  props: {
    poll_id: Number,
  },
  setup: function (props) {
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
    const groupTexts = ref([]);
    const entries = ref([]);
    const choices = ref([]);
    const updatedGroupedEntries = ref({});
    const dialogVisible = ref(false);

    const setGroupText = async (text, groupId) => {
      console.log(text);
      console.log(groupId);
      dialogVisible.value = false;
      await postGroupText(
        { group_index: groupId, poll_id: props.poll_id, text: text },
        config.value
      );
      alert("Please refresh to update the latest group introduction text.");
    };

    const md2Html = (md) => {
      if (md != null) return marked(md);
    };

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

    const isMatchingChoice = (entryId, choiceText) => (choice) =>
      choice["poll"] == entryId && choice["choice_text"] == choiceText;

    function loadlinks() {
      const len = Object.keys(groupedStudents.value).length;
      for (let i = 0; i < len; i++) {
        let locali = i;
        getFile(i + 1, config.value).then((response) => {
          links.value[locali] = response.data.file;
        });
      }
    }

    const loadGroupTexts = async () => {
      const response = await getGroups(props.poll_id);

      groupTexts.value = response.data.map((e) => e.text);

      console.log(response.data.map((e) => e.text));
    };

    // window.onpossiblyunhandledexception = function () {
    //   window.onerror.apply(this, arguments); // call
    // }

    // window.onerror = function (err) {
    //   console.log(err); // logs all errors
    // }

    const loadMyVote = async () => {
      const response = await getVote(props.poll_id, config.value);
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
      const processChoiceEntry = (entry) => {
        const { id: entryId, score } = entry;
        const choiceText = score > 0 ? score : 1;
        const choiceId = choices.value.find(
          isMatchingChoice(entryId, choiceText)
        ).id;
        return { entry: entryId, choice: choiceId, poll_id: props.poll_id };
      };

      const processTextEntry = (entry) => {
        const { id: entryId, content } = entry;
        console.log(content);
        const choiceId = choices.value.find(
          isMatchingChoice(entryId, "Enter your words")
        ).id;
        return {
          entry: entryId,
          choice: choiceId,
          content: content,
          poll_id: props.poll_id,
        };
      };

      const post = Object.values(updatedGroupedEntries.value)
        .flat()
        .reduce((accumulator, entry) => {
          if (entry.type === CHOICE_NUM.value) {
            return [...accumulator, processChoiceEntry(entry)];
          } else if (entry.type === TEXT.value) {
            return [...accumulator, processTextEntry(entry)];
          }
          return accumulator;
        }, []);

      return post;
    });

    // { "1": [ { "id": 7, "name": "student7", "net_id": "007", "user": 7, "group_index": 1 }, { "id": 8, "name": "student8", "net_id": "008", "user": 8, "group_index": 1 } ], ... }
    const groupedStudents = computed(() => {
      //https://stackoverflow.com/questions/40774697/how-can-i-group-an-array-of-objects-by-key
      const result = students.value.reduce((r, a) => {
        r[a.group_index] = r[a.group_index] || [];
        r[a.group_index].push(a);
        return r;
      }, Object.create(null));
      return result;
    });

    const groupedEntires = computed(() => {
      const result = entries.value.reduce(function (r, a) {
        r[a.group_index] = r[a.group_index] || [];
        r[a.group_index].push({
          id: a["id"],
          text: a["text"],
          group_index: a["group_index"],
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
          entries.slice().sort(myOrder),
        ])
      );

      console.log(sortedData);
      return sortedData;
    });

    const myCurrentVote = ref([]);

    const entryIdByChoiceId = (choiceId) =>
      choices.value.find((choice) => choice.id == choiceId).poll;

    const groupedMyCurrentVotes = computed(() => {
      if (!loggedIn.value) return {};
      const result_0 = myCurrentVote.value.map((m) => ({
        group_index: entries.value.find(
          (e) => e.id == entryIdByChoiceId(m.choice)
        ).group_index,
        entry: entries.value.find((e) => e.id == entryIdByChoiceId(m.choice))
          .text,
        type: entries.value.find((e) => e.id == entryIdByChoiceId(m.choice))
          .type,
        id: m.id,
        choice: choices.value.find((e) => e.id == m.choice).choice_text,
        content: m.content,
      }));
      const result = result_0.reduce((acc, curr) => {
        const { group_index, entry, type, choice, content } = curr;
        return {
          ...acc,
          [group_index]: [
            ...(acc[group_index] || []),
            { entry, type, choice, content },
          ],
        };
      }, Object.create(null));
      // reorder to  ["Delivery", "Content", "Engagement", "Any other words"];
      const sortedData = Object.fromEntries(
        Object.entries(result).map(([key, arr]) => [
          key,
          arr
            .slice()
            .sort((a, b) => ORDER.indexOf(a.entry) - ORDER.indexOf(b.entry)),
        ])
      );

      return sortedData;
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
      groupTexts,
      entries,
      groupedEntires,
      choices,
      updatedGroupedEntries,
      postVotePayload,
      groupedMyCurrentVotes,
      token,
      loggedIn,
      myCurrentVotePks,
      myCurrentVote,
      CHOICE_NUM,
      TEXT,
      ORDER,
      dialogVisible,
      setGroupText,
      md2Html,
      loadMyVote,
      uploadFile,
      submitFile,
      loadlinks,
      postVotes,
      isMatchingChoice,
      loadGroupTexts,
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

    preview() {
      this.loadGroupTexts();
      // console.log(this.postVotePayload);
    },

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
      this.loginInfo = (
        await getCurrentUserInfo(this.poll_id, this.config)
      ).data;
      this.loggedIn = true;
      const responses = await Promise.all([
        getChoices(this.config),
        getEntries(this.config, this.poll_id),
        getStudents(this.config),
        this.loadGroupTexts(),
      ]);
      this.choices = responses[0].data;
      this.entries = responses[1].data;
      this.students = responses[2].data;
      this.updatedGroupedEntries = this.groupedEntires;
      console.log(this.groupedEntires);
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
    // console.log(this.token)
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

.group_text {
  background-color: #f0f8ff;
}

/* li {} */

/* min css */
</style>
