<script>
import { useMessage } from "naive-ui";
import { defineComponent } from "vue";
import dayjs from 'dayjs'
export default defineComponent({
  name: 'RSS',
  data() {
    return {
      rssList: []
    }
  },
  setup() {
    const message = useMessage();
    return {
      success(text) {
        message.success(text)
      },
      error(text) {
        message.error(text)
      }
    }
  },
  created() {
    this.fetchRSS()
  },
  methods: {
    async fetchRSS() {
      try {
        const response = await fetch('/api/homeData.js')
        if (!response.ok) {
          throw new Error('网络请求失败');
        }
        // 将响应数据解析为JSON格式
        const responseData = await response.json();
        if (responseData?.success) {
          let data = responseData.data
          data.map((item) => {
            item.loading = false
            item.infoType = 'info'
          })
          this.rssList = data
        }
      } catch (error) {
        console.error('发生错误:', error);
      }
    },
    doCopy(item) {
      // 创建一个临时的输入元素
      let host = window.location.host
      const input = document.createElement('input');
      input.value = host + '/api/jsonfeed?series=' + item.id; // 将 item.link 赋值给输入元素
      document.body.appendChild(input); // 将输入元素添加到文档中
      input.select(); // 选中输入元素的内容
      document.execCommand('copy'); // 执行复制命令
      document.body.removeChild(input); // 移除临时输入元素
      this.success('复制成功')
    },
    async fetchQuery(item) {
      item.loading = true
      try {
        let result = await fetch(`/api/scrapyer?series=${item.id}`)
        if (!result.ok) {
          this.error('网络请求失败');
          throw new Error('网络请求失败');
        }
        const data = await result.json();
        if (data?.success) {
          item.infoType = 'success'
          item.last_update_time = dayjs().format('YYYY-MM-DD')
          this.success('查询成功')
        } else {
          item.infoType = 'error'
          this.error(data?.message || '查询失败，请稍后再试');
        }
      } catch (error) {
        console.error('发生错误:', error);
        this.error('查询失败，请稍后再试');
      }
      item.loading = false
    },

  }
})

</script>

<template>
  <n-list class="rss-list">
    <n-list-item class="rss-item" v-for="(item, index) in rssList" :key="index">
      <n-spin :show="item.loading">
        <n-alert :show-icon="false" :title="item.title" :type="item.infoType">
          <n-tag v-show="item.last_update_time" type="success">
            {{ item.last_update_time }}
          </n-tag>
        </n-alert>

      </n-spin>
      <template #suffix>

        <div class="btns">
          <n-button @click="fetchQuery(item)"
            :loading="item.loading">查询</n-button>
          <n-button @click="doCopy(item)">复制</n-button>
        </div>
      </template>
    </n-list-item>
  </n-list>
  <n-message-provider />
</template>

<style scoped>
.rss-list {
  padding: 20px;
}

.btns {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 5px;
}


.rss-item {
  /* margin: 10px 0; */
}
</style>
