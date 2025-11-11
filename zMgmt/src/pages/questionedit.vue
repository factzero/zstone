<template>
  <div class="w-full h-full p-6 bg-gray-50">
    <div class="w-full flex gap-6 h-full">
      <!-- Question Editor (Left Side) -->
      <el-card class="flex-1 flex flex-col">
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-bold">题目录入</h2>
            <el-button type="primary" @click="saveQuestion">保存题目</el-button>
          </div>
        </template>

        <div class="editor-container overflow-auto flex-grow">
          <el-form
            :model="questionForm"
            label-width="100px"
            label-position="left"
          >
            <!-- Question Type Selector -->
            <el-form-item label="题目类型">
              <el-select
                v-model="questionForm.type"
                placeholder="请选择题目类型"
                @change="onTypeChange"
              >
                <el-option label="单选题" value="single"></el-option>
                <el-option label="复合题" value="multiple"></el-option>
                <el-option label="简答题" value="shortAnswer"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="题目出处">
              <el-input
                v-model="questionForm.source"
                placeholder="请输入题目出处（如：2025年11月第8题）"
              />
            </el-form-item>

            <!-- Question Domain -->
            <el-form-item label="题目领域">
              <div class="flex gap-2">
                <el-select
                  v-model="selectedDomainCategory"
                  placeholder="领域类别"
                  clearable
                  @change="handleCategoryChange"
                  class="flex-1"
                >
                  <el-option
                    v-for="category in domainCategories"
                    :key="category.value"
                    :label="category.label"
                    :value="category.value"
                  />
                </el-select>

                <el-select
                  v-model="questionForm.subdomain"
                  placeholder="具体领域"
                  clearable
                  filterable
                  :disabled="!selectedDomainCategory"
                  class="flex-1"
                >
                  <el-option
                    v-for="subDomain in filteredSubDomains"
                    :key="subDomain.label"
                    :label="subDomain.label"
                    :value="subDomain.label"
                  />
                </el-select>
              </div>
            </el-form-item>

            <!-- 题目内容输入框 -->
            <el-form-item label="题目内容">
              <el-input
                v-model="questionForm.content"
                type="textarea"
                autosize
                placeholder="请输入题目内容，支持Markdown格式"
              />
            </el-form-item>

            <!-- Options for Single Choice -->
            <div v-if="questionForm.type === 'single'">
              <el-form-item label="选项设置">
                <el-button @click="addOption" size="small">添加选项</el-button>
              </el-form-item>

              <div class="ml-24 space-y-3 max-h-96 overflow-y-auto pr-2">
                <div
                  v-for="(option, index) in questionForm.options"
                  :key="index"
                  class="flex items-center space-x-2"
                >
                  <el-radio
                    v-model="questionForm.correctAnswer"
                    :value="index"
                    class="mr-2"
                  />
                  <span class="font-medium">{{ getOptionLabel(index) }}.</span>
                  <el-input
                    v-model="option.content"
                    placeholder="请输入选项内容"
                    type="textarea"
                    autosize
                    class="flex-1"
                  />

                  <el-button
                    @click="removeOption(index)"
                    type="danger"
                    :icon="Delete"
                    circle
                    size="small"
                  />
                </div>
              </div>
            </div>

            <!-- Sub Questions for Composite Question -->
            <div v-if="questionForm.type === 'multiple'">
              <el-form-item label="小题设置">
                <el-button @click="addSubQuestion" size="small"
                  >添加小题</el-button
                >
              </el-form-item>

              <div class="ml-24 space-y-6 max-h-96 overflow-y-auto pr-2">
                <el-card
                  v-for="(subQuestion, subIndex) in questionForm.subQuestions"
                  :key="subIndex"
                  class="mb-4"
                >
                  <template #header>
                    <div class="flex justify-between items-center">
                      <span class="font-medium">第{{ subIndex + 1 }}题</span>
                      <el-button
                        @click="removeSubQuestion(subIndex)"
                        type="danger"
                        :icon="Delete"
                        circle
                        size="small"
                      />
                    </div>
                  </template>

                  <!-- Removed 小题内容 form item -->

                  <el-form-item label="选项" label-width="80px">
                    <el-button @click="addSubOption(subIndex)" size="small"
                      >添加选项</el-button
                    >
                  </el-form-item>

                  <div class="space-y-2 ml-2">
                    <div
                      v-for="(option, optionIndex) in subQuestion.options"
                      :key="optionIndex"
                      class="flex items-center space-x-2"
                    >
                      <el-radio
                        v-model="subQuestion.correctAnswer"
                        :value="optionIndex"
                        class="mr-2"
                      />
                      <span class="font-medium"
                        >{{ getOptionLabel(optionIndex) }}.</span
                      >
                      <el-input
                        v-model="option.content"
                        placeholder="请输入选项内容"
                        type="textarea"
                        autosize
                        class="flex-1"
                      />

                      <el-button
                        @click="removeSubOption(subIndex, optionIndex)"
                        type="danger"
                        :icon="Delete"
                        circle
                        size="small"
                      />
                    </div>
                  </div>
                </el-card>
              </div>
            </div>

            <!-- 参考答案输入框 -->
            <el-form-item
              v-if="questionForm.type === 'shortAnswer'"
              label="参考答案"
            >
              <el-input
                v-model="questionForm.answer"
                type="textarea"
                autosize
                placeholder="请输入参考答案"
              />
            </el-form-item>

            <!-- 题目解析输入框 -->
            <el-form-item label="题目解析" class="py-4">
              <el-input
                v-model="questionForm.explanation"
                type="textarea"
                autosize
                placeholder="请输入题目解析（可选），支持Markdown格式"
              />
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <!-- Question Preview (Right Side) -->
      <el-card class="flex-1 flex flex-col">
        <template #header>
          <h2 class="text-xl font-bold">题目预览</h2>
        </template>

        <div class="preview-container overflow-auto flex-grow">
          <p v-if="questionForm.source">
            <strong>出处：</strong>{{ questionForm.source }}
          </p>
          <p v-if="questionForm.domain">
            <strong>领域：</strong>
            <span
              >{{ questionForm.domain
              }}{{
                questionForm.subdomain ? " - " + questionForm.subdomain : ""
              }}</span
            >
          </p>
          <!-- Single Choice Preview -->
          <div v-if="questionForm.type === 'single'" class="preview-question">
            <div class="question-content mb-4">
              <p><strong>题目：</strong></p>
              <div
                class="markdown-content"
                v-html="
                  renderMarkdown(questionForm.content || '请输入题目内容')
                "
              ></div>
            </div>

            <!-- 单选题选项预览 -->
            <div
              v-for="(option, index) in questionForm.options"
              :key="index"
              class="option-item mb-2"
              :class="{
                'correct-answer': index === questionForm.correctAnswer,
              }"
            >
              <div>
                {{ getOptionLabel(index) }}.
                {{ option.content || "请输入选项内容" }}
              </div>
            </div>

            <div class="explanation mt-4" v-if="questionForm.explanation">
              <p><strong>解析：</strong></p>
              <div
                class="markdown-content"
                v-html="renderMarkdown(questionForm.explanation)"
              ></div>
            </div>
          </div>

          <!-- Multiple Questions Preview -->
          <div
            v-else-if="questionForm.type === 'multiple'"
            class="preview-question"
          >
            <div class="question-content mb-4">
              <p><strong>题目：</strong></p>
              <div
                class="markdown-content"
                v-html="
                  renderMarkdown(questionForm.content || '请输入题目内容')
                "
              ></div>
            </div>

            <div
              v-for="(subQuestion, subIndex) in questionForm.subQuestions"
              :key="subIndex"
              class="sub-question border-b pb-4 mb-4"
            >
              <!-- Added question number indicator -->
              <p class="mb-2">
                <strong>第{{ subIndex + 1 }}题</strong>
              </p>

              <!-- 复合题子选项预览 -->
              <div class="sub-options ml-4">
                <div
                  v-for="(option, optionIndex) in subQuestion.options"
                  :key="optionIndex"
                  class="option-item mb-1"
                  :class="{
                    'correct-answer': optionIndex === subQuestion.correctAnswer,
                  }"
                >
                  <div>
                    {{ getOptionLabel(optionIndex) }}.
                    {{ option.content || "请输入选项内容" }}
                  </div>
                </div>
              </div>
            </div>

            <div class="explanation mt-4" v-if="questionForm.explanation">
              <p><strong>解析：</strong></p>
              <div
                class="markdown-content"
                v-html="renderMarkdown(questionForm.explanation)"
              ></div>
            </div>
          </div>

          <!-- Short Answer Preview -->
          <div
            v-else-if="questionForm.type === 'shortAnswer'"
            class="preview-question"
          >
            <div class="question-content mb-4">
              <p><strong>题目：</strong></p>
              <div
                class="markdown-content"
                v-html="
                  renderMarkdown(questionForm.content || '请输入题目内容')
                "
              ></div>
            </div>

            <div class="answer-preview mb-4">
              <p><strong>参考答案：</strong></p>
              <div class="answer-content mt-2 p-2 bg-gray-100 rounded">
                {{ questionForm.answer || "请输入参考答案" }}
              </div>
            </div>

            <div class="explanation" v-if="questionForm.explanation">
              <p><strong>解析：</strong></p>
              <div
                class="markdown-content"
                v-html="renderMarkdown(questionForm.explanation)"
              ></div>
            </div>
          </div>

          <!-- Default Preview -->
          <div v-else class="preview-question">
            <p>请选择题目类型以查看预览</p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, computed, watch } from "vue";
import { ElMessage } from "element-plus";
import { Delete } from "@element-plus/icons-vue";
import MarkdownIt from "markdown-it";

const domainData = [
  {
    value: "exampaper",
    label: "试卷",
    children: [
      { label: "软件工程" },
      { label: "系统分析与设计" },
      { label: "架构设计" },
      { label: "操作系统" },
    ],
  },
  {
    value: "tutorial",
    label: "教程",
    children: [
      { label: "语文" },
      { label: "英语" },
      { label: "历史" },
      { label: "地理" },
      { label: "政治" },
    ],
  },
];

// Reactive variables
const selectedDomainCategory = ref("");
const filteredSubDomains = ref<{ label: string }[]>([]);

// Computed property for domain categories
const domainCategories = computed(() => {
  return domainData.map((category) => ({
    value: category.value,
    label: category.label,
  }));
});

// Watch for changes to category selection
watch(selectedDomainCategory, (newVal) => {
  // Reset subdomain when category changes
  questionForm.subdomain = "";

  if (!newVal) {
    questionForm.domain = "";
    filteredSubDomains.value = [];
    return;
  }

  // Find the selected category and update sub-domains
  const category = domainData.find((cat) => cat.value === newVal);
  if (category) {
    questionForm.domain = category.label; // Set the domain label
    filteredSubDomains.value = category.children;
  } else {
    questionForm.domain = "";
    filteredSubDomains.value = [];
  }
});

// Handle category change (kept for backward compatibility)
const handleCategoryChange = (categoryValue: string) => {
  // Reset subdomain when category changes
  questionForm.subdomain = "";

  if (!categoryValue) {
    questionForm.domain = "";
    filteredSubDomains.value = [];
    return;
  }

  // Find the selected category and update sub-domains
  const category = domainData.find((cat) => cat.value === categoryValue);
  if (category) {
    questionForm.domain = category.label; // Set the domain label
    filteredSubDomains.value = category.children;
  } else {
    questionForm.domain = "";
    filteredSubDomains.value = [];
  }
};

// Initialize MarkdownIt
const md = new MarkdownIt({
  html: true, // 允许 HTML 标签
  xhtmlOut: true, // 使用 '/' 来闭合单标签 (比如 <br />)
  breaks: true, // 转换段落里的 '\n' 到 <br>
  linkify: true, // 自动识别 URL 为链接
  typographer: true, // 启用一些语言中立的替换 + 引号美化
  quotes: "\"\"''", // 引号替换对，当 typographer 启用时
});

// Function to render Markdown
const renderMarkdown = (content: string) => {
  if (!content.trim()) return content;
  return md.render(content);
};

// Define question form structure
const questionForm = reactive({
  type: "single",
  content: "",
  source: "",
  domain: "",
  subdomain: "",
  options: [] as { content: string; isCorrect: boolean }[],
  correctAnswer: 0,
  subQuestions: [] as {
    content: string;
    options: { content: string }[];
    correctAnswer: number;
  }[],
  answer: "",
  explanation: "",
});

// Add a new option for single choice
const addOption = () => {
  questionForm.options.push({
    content: "",
    isCorrect: false,
  });
};

// Remove an option for single choice
const removeOption = (index: number) => {
  questionForm.options.splice(index, 1);

  // Adjust correct answer index if needed
  if (questionForm.correctAnswer >= questionForm.options.length) {
    questionForm.correctAnswer = Math.max(0, questionForm.options.length - 1);
  }
};

// Add a new sub-question for composite question
const addSubQuestion = () => {
  questionForm.subQuestions.push({
    content: "",
    options: [],
    correctAnswer: 0,
  });
};

// Remove a sub-question
const removeSubQuestion = (index: number) => {
  questionForm.subQuestions.splice(index, 1);
};

// Add option to a sub-question
const addSubOption = (subIndex: number) => {
  const subQuestion = questionForm.subQuestions[subIndex];
  if (subQuestion) {
    subQuestion.options.push({ content: "" });
  }
};

// Remove option from a sub-question
const removeSubOption = (subIndex: number, optionIndex: number) => {
  const subQuestion = questionForm.subQuestions[subIndex];
  if (subQuestion) {
    subQuestion.options.splice(optionIndex, 1);

    // Adjust correct answer index if needed
    if (subQuestion.correctAnswer >= subQuestion.options.length) {
      subQuestion.correctAnswer = Math.max(0, subQuestion.options.length - 1);
    }
  }
};

// Handle question type change
const onTypeChange = () => {
  // Reset all fields when changing type
  questionForm.options = [];
  questionForm.correctAnswer = 0;
  questionForm.subQuestions = [];
  questionForm.answer = "";

  // Add default options for single choice
  if (questionForm.type === "single") {
    addOption();
    addOption();
    addOption();
    addOption();
  }
};

// Get option label (A, B, C, D, ...)
const getOptionLabel = (index: number) => {
  return String.fromCharCode(65 + index); // 65 is ASCII code for 'A'
};

// Save question
const saveQuestion = () => {
  // Validation
  if (!questionForm.content.trim()) {
    ElMessage.error("请输入题目内容");
    return;
  }

  if (questionForm.type === "single") {
    if (questionForm.options.some((opt) => !opt.content.trim())) {
      ElMessage.error("请完善所有选项内容");
      return;
    }

    if (
      !questionForm.options.some(
        (_, index) => index === questionForm.correctAnswer,
      )
    ) {
      ElMessage.error("请选择正确答案");
      return;
    }
  }

  if (questionForm.type === "multiple") {
    if (questionForm.subQuestions.length === 0) {
      ElMessage.error("请至少添加一个小题");
      return;
    }

    for (let i = 0; i < questionForm.subQuestions.length; i++) {
      const subQuestion = questionForm.subQuestions[i];

      // Add this check to ensure subQuestion is defined
      if (!subQuestion) continue;

      // Removed validation for subQuestion.content since we removed the field

      if (subQuestion.options.length < 2) {
        ElMessage.error(`第${i + 1}个小题至少需要两个选项`);
        return;
      }

      if (subQuestion.options.some((opt) => !opt.content.trim())) {
        ElMessage.error(`第${i + 1}个小题请完善所有选项内容`);
        return;
      }

      if (
        !subQuestion.options.some(
          (_, index) => index === subQuestion.correctAnswer,
        )
      ) {
        ElMessage.error(`第${i + 1}个小题请选择正确答案`);
        return;
      }
    }
  }

  if (questionForm.type === "shortAnswer" && !questionForm.answer.trim()) {
    ElMessage.error("请输入参考答案");
    return;
  }

  // 生成 JSON 格式
  const questionAsJson = JSON.stringify(questionForm, null, 2);

  // 可以显示给用户或用于保存
  console.log("题目JSON格式:", questionAsJson);

  // 保存逻辑...
  ElMessage.success("题目保存成功");
};
</script>

<style scoped>
.editor-container,
.preview-container {
  height: calc(100vh - 180px);
}

.preview-question {
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 4px;
  min-height: 400px;
}

.option-item {
  padding: 0.25rem 0;
}

.sub-question:last-child {
  border-bottom: none;
}

.markdown-content :deep(*) {
  max-width: 100%;
}

.markdown-content :deep(h1) {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.markdown-content :deep(h2) {
  font-size: 1.3rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.markdown-content :deep(h3) {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.markdown-content :deep(p) {
  margin: 0.5rem 0;
}

.markdown-content :deep(ul) {
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

.markdown-content :deep(ol) {
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

.markdown-content :deep(li) {
  margin: 0.25rem 0;
}

.markdown-content :deep(code) {
  background-color: #eaeaea;
  padding: 0.1rem 0.3rem;
  border-radius: 0.2rem;
  font-family: monospace;
}

.markdown-content :deep(pre) {
  background-color: #eaeaea;
  padding: 0.5rem;
  border-radius: 0.2rem;
  overflow-x: auto;
}

.markdown-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #ccc;
  padding-left: 1rem;
  margin: 0.5rem 0;
  color: #666;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 0.5rem 0;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  border: 1px solid #ddd;
  padding: 0.25rem;
  text-align: left;
}

.markdown-content :deep(th) {
  background-color: #f5f5f5;
}

.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
}

.markdown-content :deep(strong) {
  font-weight: bold;
}

.markdown-content :deep(em) {
  font-style: italic;
}

.markdown-content :deep(del) {
  text-decoration: line-through;
}

.markdown-content :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}

.markdown-content :deep(hr) {
  border: none;
  border-top: 1px solid #eaeaea;
  margin: 1rem 0;
}

/* 正确答案高亮样式 */
.correct-answer {
  background-color: #f0f9ff;
  border-left: 4px solid #409eff;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  margin-left: -0.5rem;
}

.correct-answer .el-radio__label {
  color: #409eff;
  font-weight: bold;
}

/* 暗黑模式样式 */
.dark .preview-question {
  background-color: #1e1e1e;
  color: #e0e0e0;
}

.dark .preview-question strong {
  color: #ffffff;
}

.dark .correct-answer {
  background-color: #1a3c5e;
  border-left: 4px solid #409eff;
}

.dark .correct-answer div {
  color: #63b3ed;
}

.dark .sub-question {
  border-bottom: 1px solid #444;
}

.dark .answer-content {
  background-color: #2d2d2d !important;
  color: #e0e0e0;
}

.dark .markdown-content :deep(h1),
.dark .markdown-content :deep(h2),
.dark .markdown-content :deep(h3),
.dark .markdown-content :deep(h4),
.dark .markdown-content :deep(h5),
.dark .markdown-content :deep(h6),
.dark .markdown-content :deep(p),
.dark .markdown-content :deep(li) {
  color: #e0e0e0;
}

.dark .markdown-content :deep(code),
.dark .markdown-content :deep(pre) {
  background-color: #2d2d2d;
  color: #e0e0e0;
}

.dark .markdown-content :deep(blockquote) {
  border-left: 4px solid #444;
  color: #b0b0b0;
}

.dark .markdown-content :deep(table) {
  color: #e0e0e0;
}

.dark .markdown-content :deep(th) {
  background-color: #2d2d2d;
  color: #e0e0e0;
}

.dark .markdown-content :deep(td) {
  border: 1px solid #444;
}

.dark .option-item {
  color: #e0e0e0;
}
</style>
