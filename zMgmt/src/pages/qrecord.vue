<!-- QuestionInput.vue -->
<template>
  <div class="flex h-screen bg-gray-50">
    <!-- 左侧录入区域 -->
    <div class="w-1/2 p-6 overflow-y-auto border-r">
      <h1 class="text-2xl font-bold mb-6 text-gray-800">题目录入</h1>

      <!-- 题目类型选择 -->
      <el-form :model="questionForm" label-width="auto">
        <!-- 出处和领域 -->
        <div class="flex space-x-4">
          <el-form-item label="出处" class="flex-1">
            <el-input
              v-model="questionForm.source"
              placeholder="请输入题目出处"
            ></el-input>
          </el-form-item>
          <el-form-item label="领域" class="flex-1">
            <el-input
              v-model="questionForm.domain"
              placeholder="请输入题目领域"
            ></el-input>
          </el-form-item>
        </div>

        <el-form-item label="类型">
          <el-select v-model="questionForm.type" @change="handleTypeChange">
            <el-option label="综合知识" value="comprehensive"></el-option>
            <el-option label="案例分析" value="caseAnalysis"></el-option>
            <el-option label="论文题目" value="thesis"></el-option>
          </el-select>
        </el-form-item>

        <!-- 题干输入 -->
        <el-form-item label="题干">
          <el-input
            type="textarea"
            v-model="questionForm.stem"
            :rows="4"
            placeholder="请输入题干内容，支持Markdown语法"
          ></el-input>
        </el-form-item>

        <!-- 不同题型的特殊处理 -->
        <div v-if="questionForm.type === 'comprehensive'">
          <el-divider>选择题部分</el-divider>

          <div
            v-for="(choice, index) in questionForm.choices"
            :key="index"
            class="mb-4 p-4 border rounded"
          >
            <div class="flex justify-between items-center mb-2">
              <h3 class="font-medium">第{{ index + 1 }}题</h3>
              <el-button type="danger" link @click="removeChoice(index)"
                >删除</el-button
              >
            </div>

            <div
              v-for="(option, optIndex) in choice.options"
              :key="optIndex"
              class="flex items-center mb-2"
            >
              <el-radio
                v-model="choice.correctAnswer"
                :value="optIndex"
                class="mr-2"
              ></el-radio>
              <span class="mr-2"
                >{{ String.fromCharCode(65 + optIndex) }}.</span
              >
              <el-input
                v-model="option.text"
                type="textarea"
                placeholder="选项内容"
                class="flex-1"
              ></el-input>
              <el-button
                type="danger"
                link
                @click="removeOption(index, optIndex)"
                class="ml-2"
                >删除</el-button
              >
            </div>

            <div class="flex space-x-2 mt-2">
              <el-button @click="addOption(index)">添加选项</el-button>
            </div>
          </div>

          <el-button @click="addChoice" type="primary" class="w-full"
            >添加选择题</el-button
          >

          <el-divider class="mt-6">题目解析</el-divider>
          <el-form-item label="解析">
            <el-input
              type="textarea"
              v-model="questionForm.analysis"
              :rows="4"
              placeholder="请输入题目解析，支持Markdown语法"
            ></el-input>
          </el-form-item>
        </div>

        <div v-else-if="questionForm.type === 'caseAnalysis'">
          <el-divider>小问题部分</el-divider>

          <div
            v-for="(subQuestion, index) in questionForm.subQuestions"
            :key="index"
            class="mb-4 p-4 border rounded"
          >
            <div class="flex justify-between items-center mb-2">
              <h3 class="font-medium">问题{{ index + 1 }}</h3>
              <el-button type="danger" link @click="removeSubQuestion(index)"
                >删除</el-button
              >
            </div>

            <el-input
              type="textarea"
              v-model="subQuestion.question"
              :rows="2"
              placeholder="请输入问题"
              class="mb-2"
            ></el-input>

            <el-input
              type="textarea"
              v-model="subQuestion.answer"
              :rows="3"
              placeholder="请输入参考答案"
            ></el-input>

            <el-input
              type="textarea"
              v-model="subQuestion.analysis"
              :rows="3"
              placeholder="请输入题目解析，支持Markdown语法"
            ></el-input>
          </div>

          <el-button @click="addSubQuestion" type="primary" class="w-full"
            >添加小问题</el-button
          >
        </div>

        <div v-else-if="questionForm.type === 'thesis'">
          <el-divider>论文题目解析</el-divider>
          <el-form-item label="解析">
            <el-input
              type="textarea"
              v-model="questionForm.analysis"
              :rows="6"
              placeholder="请输入论文题目解析，支持Markdown语法"
            ></el-input>
          </el-form-item>
        </div>
      </el-form>

      <div class="flex justify-end space-x-3 mt-6">
        <el-button @click="resetForm">重置</el-button>
        <el-button type="primary" @click="saveQuestion" :loading="isSaving">
          {{ isSaving ? "保存中..." : "保存题目" }}
        </el-button>
      </div>
    </div>

    <!-- 右侧预览区域 -->
    <div class="w-1/2 p-6 overflow-y-auto bg-white">
      <h1 class="text-2xl font-bold mb-6 text-gray-800">题目预览</h1>

      <div class="preview-content prose max-w-none">
        <!-- 题目信息 -->
        <div class="grid grid-cols-2 gap-4 mb-6">
          <div>
            <h3 class="text-sm font-medium text-gray-500">出处</h3>
            <p>{{ questionForm.source || "未填写" }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500">领域</h3>
            <p>{{ questionForm.domain || "未填写" }}</p>
          </div>
        </div>

        <!-- 题干预览 -->
        <div class="mb-6">
          <h2 class="text-lg font-semibold mb-2">题干</h2>
          <div
            class="p-4 bg-gray-50 rounded"
            v-html="renderMarkdown(questionForm.stem)"
          ></div>
        </div>

        <!-- 不同题型预览 -->
        <div v-if="questionForm.type === 'comprehensive'">
          <h2 class="text-lg font-semibold mb-4">选择题部分</h2>

          <div
            v-for="(choice, index) in questionForm.choices"
            :key="index"
            class="mb-6 p-4 border rounded"
          >
            <h3 class="font-medium mb-3">第{{ index + 1 }}题：</h3>

            <div class="flex flex-col gap-4">
              <div
                v-for="(option, optIndex) in choice.options"
                :key="optIndex"
                :class="[
                  'flex items-start p-3 rounded border',
                  choice.correctAnswer === optIndex
                    ? 'bg-green-100 border-green-300'
                    : 'hover:bg-gray-50 border-gray-200',
                ]"
              >
                <span
                  :class="[
                    'font-medium mr-2 flex-shrink-0',
                    choice.correctAnswer === optIndex ? 'text-green-700' : '',
                  ]"
                >
                  {{ String.fromCharCode(65 + optIndex) }}.
                </span>
                <span
                  v-html="renderMarkdown(option.text)"
                  class="flex-grow"
                ></span>
                <el-tag
                  v-if="choice.correctAnswer === optIndex"
                  type="success"
                  size="small"
                  class="ml-2 flex-shrink-0"
                >
                  正确答案
                </el-tag>
              </div>
            </div>
          </div>

          <div class="mt-6">
            <h2 class="text-lg font-semibold mb-2">题目解析</h2>
            <div
              class="p-4 bg-gray-50 rounded"
              v-html="renderMarkdown(questionForm.analysis)"
            ></div>
          </div>
        </div>

        <div v-else-if="questionForm.type === 'caseAnalysis'">
          <h2 class="text-lg font-semibold mb-4">问题部分</h2>

          <div
            v-for="(subQuestion, index) in questionForm.subQuestions"
            :key="index"
            class="mb-6 p-4 border rounded"
          >
            <h3 class="font-medium mb-3">
              问题{{ index + 1 }}：{{ subQuestion.question }}
            </h3>
            <div class="mt-2 p-3 bg-blue-50 rounded">
              <p class="font-medium text-blue-700">参考答案：</p>
              <div v-html="renderMarkdown(subQuestion.answer)"></div>
            </div>
          </div>
        </div>

        <div v-else-if="questionForm.type === 'thesis'">
          <h2 class="text-lg font-semibold mb-2">题目解析</h2>
          <div
            class="p-4 bg-gray-50 rounded"
            v-html="renderMarkdown(questionForm.analysis)"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import MarkdownIt from "markdown-it";

// 选择题接口
interface Choice {
  options: { text: string }[];
  correctAnswer: number;
}

// 小问题接口
interface SubQuestion {
  question: string;
  answer: string;
  analysis: string;
}

// 题目数据接口
interface QuestionData {
  type: "comprehensive" | "caseAnalysis" | "thesis";
  stem: string;
  source: string;
  domain: string;
  choices: Choice[];
  subQuestions: SubQuestion[];
  analysis: string;
}

// 初始化Markdown解析器
const md = new MarkdownIt();

// 加载状态
const isSaving = ref(false);

// 表单数据
const questionForm = reactive<QuestionData>({
  type: "comprehensive",
  stem: "",
  source: "",
  domain: "",
  choices: [],
  subQuestions: [],
  analysis: "",
});

// 处理题目类型变化
const handleTypeChange = () => {
  // 清空特定类型的字段
  questionForm.choices = [];
  questionForm.subQuestions = [];
  questionForm.analysis = "";
};

// 添加选择题
const addChoice = () => {
  questionForm.choices.push({
    options: [{ text: "" }, { text: "" }],
    correctAnswer: 0,
  });
};

// 删除选择题
const removeChoice = (index: number) => {
  questionForm.choices.splice(index, 1);
};

// 删除选项的方法
const removeOption = (choiceIndex: number, optionIndex: number) => {
  if (questionForm.choices[choiceIndex]) {
    const choice = questionForm.choices[choiceIndex];
    if (choice.options.length > 2) {
      // 确保至少有2个选项
      choice.options.splice(optionIndex, 1);

      // 如果删除的是当前正确答案，则将正确答案设为第一个选项
      if (choice.correctAnswer === optionIndex) {
        choice.correctAnswer = 0;
      }
      // 如果删除的选项在正确答案之前，需要更新正确答案索引
      else if (optionIndex < choice.correctAnswer) {
        // 将正确答案索引减1
        choice.correctAnswer = choice.correctAnswer - 1;
      }
      // 如果删除的选项在正确答案之后，不需要更改正确答案索引
    } else {
      ElMessage({ message: "选项不能少于2个", type: "warning" });
    }
  }
};

// 添加选项
const addOption = (choiceIndex: number) => {
  if (questionForm.choices[choiceIndex]) {
    questionForm.choices[choiceIndex].options.push({ text: "" });
  }
};

// 添加小问题
const addSubQuestion = () => {
  questionForm.subQuestions.push({
    question: "",
    answer: "",
    analysis: "",
  });
};

// 删除小问题
const removeSubQuestion = (index: number) => {
  questionForm.subQuestions.splice(index, 1);
};

// 重置表单
const resetForm = () => {
  questionForm.stem = "";
  questionForm.source = "";
  questionForm.domain = "";
  questionForm.choices = [];
  questionForm.subQuestions = [];
  questionForm.analysis = "";
};

// 验证表单数据
const validateForm = (): boolean => {
  if (!questionForm.stem.trim()) {
    ElMessage({ message: "请输入题干内容", type: "error" });
    return false;
  }

  if (questionForm.type === "comprehensive") {
    if (questionForm.choices.length === 0) {
      ElMessage({ message: "请添加至少一道选择题", type: "error" });
      return false;
    }

    for (let i = 0; i < questionForm.choices.length; i++) {
      const choice = questionForm.choices[i];
      if (choice && choice.options?.some((opt) => !opt.text?.trim())) {
        ElMessage({ message: `第${i + 1}题存在空选项`, type: "error" });
        return false;
      }
    }
  }

  if (questionForm.type === "caseAnalysis") {
    if (questionForm.subQuestions.length === 0) {
      ElMessage({ message: "请添加至少一个小问题", type: "error" });
      return false;
    }

    for (let i = 0; i < questionForm.subQuestions.length; i++) {
      const subQ = questionForm.subQuestions[i];
      if (!subQ || !subQ.question?.trim() || !subQ.answer?.trim()) {
        ElMessage({
          message: `问题${i + 1}的内容和答案都不能为空`,
          type: "error",
        });
        return false;
      }
    }
  }

  return true;
};

// 发送数据到后端
const submitToBackend = async (data: QuestionData) => {
  try {
    // 构造符合后端API要求的数据格式
    const requestData = {
      type: data.type,
      stem: data.stem,
      source: data.source || null,
      domain: data.domain || null,
      choices:
        data.type === "comprehensive"
          ? data.choices.map((choice) => ({
              options: choice.options,
              correctAnswer: choice.correctAnswer,
            }))
          : null,
      subQuestions: data.type === "caseAnalysis" ? data.subQuestions : null,
      analysis: data.analysis || null,
    };

    // 发送到后端
    const response = await fetch("http://localhost:8000/api/questions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      let errorMessage = "保存失败";
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch {
        // 如果无法解析错误信息，则使用状态文本
        errorMessage = response.statusText || errorMessage;
      }
      throw new Error(errorMessage);
    }

    const result = await response.json();
    ElMessage({ message: "题目保存成功", type: "success" });
    return result;
  } catch (error) {
    const message = (error as Error).message || "未知错误";
    ElMessage({ message: `保存题目时发生错误: ${message}`, type: "error" });
    throw error;
  }
};

// 保存题目
const saveQuestion = async () => {
  // 先验证数据
  if (!validateForm()) {
    return;
  }

  isSaving.value = true;

  try {
    // 直接使用 questionForm 数据，避免创建不必要的副本
    await submitToBackend(questionForm);
    console.log("保存的题目数据:", questionForm);
  } catch (error) {
    console.error("保存失败:", error);
  } finally {
    isSaving.value = false;
  }
};

// 渲染Markdown
const renderMarkdown = (content: string) => {
  if (!content) return "";
  return md.render(content);
};
</script>

<style scoped>
.preview-content :deep(h1) {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.preview-content :deep(h2) {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.preview-content :deep(h3) {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.preview-content :deep(p) {
  margin-bottom: 0.5rem;
}

.preview-content :deep(code) {
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

.preview-content :deep(pre) {
  background-color: #f3f4f6;
  padding: 1rem;
  border-radius: 0.25rem;
  overflow-x: auto;
}

.preview-content :deep(blockquote) {
  border-left: 4px solid #d1d5db;
  padding-left: 1rem;
  margin-left: 0;
  color: #6b7280;
}

.preview-content :deep(ul),
.preview-content :deep(ol) {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.preview-content :deep(li) {
  margin-bottom: 0.25rem;
}

.preview-content :deep(strong) {
  font-weight: 600;
}

.preview-content :deep(em) {
  font-style: italic;
}
</style>
