<template>
  <el-dialog
    :model-value="dialogVisible"
    title="Edit Group Introduction"
    width="30%"
    :lock-scroll="false"
  >
    <h3>Group introduction, markdown supported</h3>
    <!-- {{ key }} -->
    <textarea v-model="text"></textarea>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="cancelDialog">Cancel</el-button>
        <el-button type="primary" @click="confirmDialog"> Confirm </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
export default {
  props: {
    dialogVisible: {
      type: Boolean,
      required: true,
    },
    // key: {
    //   type: String,
    //   required: true,
    // },
  },
  data() {
    return {
      text: "",
    };
  },
  methods: {
    confirmDialog() {
      this.$emit("confirmDialog", this.text);
    },
    cancelDialog() {
      this.$emit("cancelDialog");
    },
  },
};
</script>

<style>
textarea {
  margin-top: 10px;
  resize: none;
  width: 100%;
  height: 150px;
}
</style>
