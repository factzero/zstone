<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-800">试题管理</h1>
        <div class="flex space-x-3">
          <el-button @click="fetchQuestions" :icon="Refresh"> 刷新 </el-button>
          <el-button type="primary" @click="openCreateDialog" :icon="Plus">
            添加新试题
          </el-button>
        </div>
      </div>

      <!-- 试题表格 -->
      <el-table
        :data="questions"
        v-loading="loading"
        stripe
        border
        class="w-full"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeTag(scope.row.type)">
              {{ getTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="source" label="出处" show-overflow-tooltip />
        <el-table-column prop="domain" label="领域" show-overflow-tooltip />
        <el-table-column prop="stem" label="题干" show-overflow-tooltip>
          <template #default="scope">
            <div v-html="truncateMarkdown(scope.row.stem, 50)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <div class="flex space-x-2">
              <el-button size="small" @click="openPreviewDialog(scope.row)">
                预览
              </el-button>
              <el-button size="small" @click="openEditDialog(scope.row)">
                编辑
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="deleteQuestion(scope.row.id)"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="mt-6 flex justify-end">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 添加/编辑试题对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      :title="dialogMode === 'create' ? '添加新试题' : '编辑试题'"
      width="90%"
      @close="handleDialogClose"
      destroy-on-close
    >
      <div class="flex h-[70vh]">
        <!-- 录入区域 -->
        <div class="w-1/2 pr-4 overflow-y-auto border-r">
          <el-form :model="currentQuestion" label-width="auto">
            <!-- 出处和领域 -->
            <div class="flex space-x-4">
              <el-form-item label="出处" class="flex-1">
                <el-input
                  v-model="currentQuestion.source"
                  placeholder="请输入题目出处"
                ></el-input>
              </el-form-item>
              <el-form-item label="领域" class="flex-1">
                <el-input
                  v-model="currentQuestion.domain"
                  placeholder="请输入题目领域"
                ></el-input>
              </el-form-item>
            </div>

            <el-form-item label="类型">
              <el-select
                v-model="currentQuestion.type"
                :disabled="dialogMode === 'edit'"
              >
                <el-option label="综合知识" value="comprehensive"></el-option>
                <el-option label="案例分析" value="caseAnalysis"></el-option>
                <el-option label="论文题目" value="thesis"></el-option>
              </el-select>
            </el-form-item>

            <!-- 题干输入 -->
            <el-form-item label="题干">
              <el-input
                type="textarea"
                v-model="currentQuestion.stem"
                :rows="4"
                placeholder="请输入题干内容，支持Markdown语法"
              ></el-input>
            </el-form-item>

            <!-- 不同题型的特殊处理 -->
            <div v-if="currentQuestion.type === 'comprehensive'">
              <el-divider>选择题部分</el-divider>

              <div
                v-for="(choice, index) in currentQuestion.choices"
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
                  v-model="currentQuestion.analysis"
                  :rows="4"
                  placeholder="请输入题目解析，支持Markdown语法"
                ></el-input>
              </el-form-item>
            </div>

            <div v-else-if="currentQuestion.type === 'caseAnalysis'">
              <el-divider>小问题部分</el-divider>

              <div
                v-for="(subQuestion, index) in currentQuestion.subQuestions"
                :key="index"
                class="mb-4 p-4 border rounded"
              >
                <div class="flex justify-between items-center mb-2">
                  <h3 class="font-medium">问题{{ index + 1 }}</h3>
                  <el-button
                    type="danger"
                    link
                    @click="removeSubQuestion(index)"
                    >删除</el-button
                  >
                </div>

                <el-form-item label="题干" class="mb-2">
                  <el-input
                    type="textarea"
                    v-model="subQuestion.question"
                    :rows="2"
                    placeholder="请输入问题"
                  ></el-input>
                </el-form-item>

                <el-form-item label="参考答案" class="mb-2">
                  <el-input
                    type="textarea"
                    v-model="subQuestion.answer"
                    :rows="3"
                    placeholder="请输入参考答案"
                  ></el-input>
                </el-form-item>

                <el-form-item label="题目解析" class="mb-2">
                  <el-input
                    type="textarea"
                    v-model="subQuestion.analysis"
                    :rows="3"
                    placeholder="请输入题目解析，支持Markdown语法"
                  ></el-input>
                </el-form-item>
              </div>

              <el-button @click="addSubQuestion" type="primary" class="w-full"
                >添加小问题</el-button
              >
            </div>

            <div v-else-if="currentQuestion.type === 'thesis'">
              <el-divider>论文题目解析</el-divider>
              <el-form-item label="解析">
                <el-input
                  type="textarea"
                  v-model="currentQuestion.analysis"
                  :rows="6"
                  placeholder="请输入论文题目解析，支持Markdown语法"
                ></el-input>
              </el-form-item>
            </div>
          </el-form>
        </div>

        <!-- 预览区域 -->
        <div class="w-1/2 pl-4 overflow-y-auto">
          <h2 class="text-xl font-bold mb-4 text-gray-800">题目预览</h2>

          <div class="preview-content prose max-w-none">
            <!-- 题目信息 -->
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div>
                <h3 class="text-sm font-medium text-gray-500">出处</h3>
                <p>{{ currentQuestion.source || "未填写" }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-500">领域</h3>
                <p>{{ currentQuestion.domain || "未填写" }}</p>
              </div>
            </div>

            <!-- 题干预览 -->
            <div class="mb-6">
              <h2 class="text-lg font-semibold mb-2">题干</h2>
              <div
                class="p-4 bg-gray-50 rounded"
                v-html="renderMarkdown(currentQuestion.stem)"
              ></div>
            </div>

            <!-- 不同题型预览 -->
            <div v-if="currentQuestion.type === 'comprehensive'">
              <h2 class="text-lg font-semibold mb-4">选择题部分</h2>

              <div
                v-for="(choice, index) in currentQuestion.choices"
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
                        choice.correctAnswer === optIndex
                          ? 'text-green-700'
                          : '',
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
                  v-html="renderMarkdown(currentQuestion.analysis)"
                ></div>
              </div>
            </div>

            <div v-else-if="currentQuestion.type === 'caseAnalysis'">
              <h2 class="text-lg font-semibold mb-4">问题部分</h2>

              <div
                v-for="(subQuestion, index) in currentQuestion.subQuestions"
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
                <div class="mt-2 p-3 bg-blue-50 rounded">
                  <p class="font-medium text-blue-700">题目解析：</p>
                  <div v-html="renderMarkdown(subQuestion.analysis)"></div>
                </div>
              </div>
            </div>

            <div v-else-if="currentQuestion.type === 'thesis'">
              <h2 class="text-lg font-semibold mb-2">题目解析</h2>
              <div
                class="p-4 bg-gray-50 rounded"
                v-html="renderMarkdown(currentQuestion.analysis)"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveQuestion" :loading="isSaving">
            {{ isSaving ? "保存中..." : "保存题目" }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="试题预览"
      width="80%"
      destroy-on-close
    >
      <div class="max-h-[70vh] overflow-y-auto p-4">
        <div class="preview-content prose max-w-none">
          <!-- 题目信息 -->
          <div class="grid grid-cols-2 gap-4 mb-6">
            <div>
              <h3 class="text-sm font-medium text-gray-500">出处</h3>
              <p>{{ previewQuestion.source || "未填写" }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">领域</h3>
              <p>{{ previewQuestion.domain || "未填写" }}</p>
            </div>
          </div>

          <!-- 题干 -->
          <div class="mb-6">
            <h2 class="text-lg font-semibold mb-2">题干</h2>
            <div
              class="p-4 bg-gray-50 rounded"
              v-html="renderMarkdown(previewQuestion.stem)"
            ></div>
          </div>

          <!-- 不同题型预览 -->
          <div v-if="previewQuestion.type === 'comprehensive'">
            <h2 class="text-lg font-semibold mb-4">选择题部分</h2>

            <div
              v-for="(choice, index) in previewQuestion.choices"
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
                v-html="renderMarkdown(previewQuestion.analysis)"
              ></div>
            </div>
          </div>

          <div v-else-if="previewQuestion.type === 'caseAnalysis'">
            <h2 class="text-lg font-semibold mb-4">问题部分</h2>

            <div
              v-for="(subQuestion, index) in previewQuestion.subQuestions"
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

          <div v-else-if="previewQuestion.type === 'thesis'">
            <h2 class="text-lg font-semibold mb-2">题目解析</h2>
            <div
              class="p-4 bg-gray-50 rounded"
              v-html="renderMarkdown(previewQuestion.analysis)"
            ></div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Refresh, Plus } from "@element-plus/icons-vue";
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
  id?: number;
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

// 页面状态
const loading = ref(false);
const isSaving = ref(false);
const editDialogVisible = ref(false);
const previewDialogVisible = ref(false);
const dialogMode = ref<"create" | "edit">("create");

// 试题数据
const questions = ref<QuestionData[]>([]);

// 当前编辑的题目
const currentQuestion = reactive<QuestionData>({
  type: "comprehensive",
  stem: "",
  source: "",
  domain: "",
  choices: [],
  subQuestions: [],
  analysis: "",
});

// 预览的题目
const previewQuestion = ref<QuestionData>({
  type: "comprehensive",
  stem: "",
  source: "",
  domain: "",
  choices: [],
  subQuestions: [],
  analysis: "",
});

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0,
});

// 获取试题列表
const fetchQuestions = async () => {
  loading.value = true;
  try {
    const response = await fetch(
      `http://localhost:8000/api/questions?page=${pagination.currentPage}&size=${pagination.pageSize}`,
    );

    if (!response.ok) {
      throw new Error("获取试题失败");
    }

    const data = await response.json();
    questions.value = data.items || data;
    pagination.total = data.total || data.length;
  } catch (error) {
    ElMessage.error("获取试题失败: " + (error as Error).message);
  } finally {
    loading.value = false;
  }
};

// 打开创建对话框
const openCreateDialog = () => {
  dialogMode.value = "create";
  resetCurrentQuestion();
  editDialogVisible.value = true;
};

// 打开编辑对话框
const openEditDialog = (question: QuestionData) => {
  dialogMode.value = "edit";
  Object.assign(currentQuestion, JSON.parse(JSON.stringify(question)));
  editDialogVisible.value = true;
};

// 打开预览对话框
const openPreviewDialog = (question: QuestionData) => {
  previewQuestion.value = JSON.parse(JSON.stringify(question));
  previewDialogVisible.value = true;
};

// 重置当前题目
const resetCurrentQuestion = (): void => {
  Object.assign(currentQuestion, {
    type: "comprehensive",
    stem: "",
    source: "",
    domain: "",
    choices: [],
    subQuestions: [],
    analysis: "",
  });
};

// 添加选择题
const addChoice = () => {
  currentQuestion.choices.push({
    options: [{ text: "" }, { text: "" }],
    correctAnswer: 0,
  });
};

// 删除选择题
const removeChoice = (index: number) => {
  currentQuestion.choices.splice(index, 1);
};

// 删除选项的方法
const removeOption = (choiceIndex: number, optionIndex: number) => {
  if (currentQuestion.choices[choiceIndex]) {
    const choice = currentQuestion.choices[choiceIndex];
    if (choice.options.length > 2) {
      choice.options.splice(optionIndex, 1);

      if (choice.correctAnswer === optionIndex) {
        choice.correctAnswer = 0;
      } else if (optionIndex < choice.correctAnswer) {
        choice.correctAnswer = choice.correctAnswer - 1;
      }
    } else {
      ElMessage({ message: "选项不能少于2个", type: "warning" });
    }
  }
};

// 添加选项
const addOption = (choiceIndex: number) => {
  if (currentQuestion.choices[choiceIndex]) {
    currentQuestion.choices[choiceIndex].options.push({ text: "" });
  }
};

// 添加小问题
const addSubQuestion = () => {
  currentQuestion.subQuestions.push({
    question: "",
    answer: "",
    analysis: "",
  });
};

// 删除小问题
const removeSubQuestion = (index: number) => {
  currentQuestion.subQuestions.splice(index, 1);
};

// 验证表单数据
const validateForm = (): boolean => {
  if (!currentQuestion.stem.trim()) {
    ElMessage({ message: "请输入题干内容", type: "error" });
    return false;
  }

  if (currentQuestion.type === "comprehensive") {
    if (currentQuestion.choices.length === 0) {
      ElMessage({ message: "请添加至少一道选择题", type: "error" });
      return false;
    }

    for (let i = 0; i < currentQuestion.choices.length; i++) {
      const choice = currentQuestion.choices[i];
      if (choice && choice.options?.some((opt) => !opt.text?.trim())) {
        ElMessage({ message: `第${i + 1}题存在空选项`, type: "error" });
        return false;
      }
    }
  }

  if (currentQuestion.type === "caseAnalysis") {
    if (currentQuestion.subQuestions.length === 0) {
      ElMessage({ message: "请添加至少一个小问题", type: "error" });
      return false;
    }

    for (let i = 0; i < currentQuestion.subQuestions.length; i++) {
      const subQ = currentQuestion.subQuestions[i];
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

// 保存题目
const saveQuestion = async () => {
  if (!validateForm()) {
    return;
  }

  isSaving.value = true;
  try {
    const url =
      dialogMode.value === "create"
        ? "http://localhost:8000/api/questions"
        : `http://localhost:8000/api/questions/${currentQuestion.id}`;

    const method = dialogMode.value === "create" ? "POST" : "PUT";

    const requestData = {
      ...currentQuestion,
      choices:
        currentQuestion.type === "comprehensive"
          ? currentQuestion.choices
          : null,
      subQuestions:
        currentQuestion.type === "caseAnalysis"
          ? currentQuestion.subQuestions
          : null,
      analysis: currentQuestion.analysis || null,
    };

    const response = await fetch(url, {
      method,
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
        errorMessage = response.statusText || errorMessage;
      }
      throw new Error(errorMessage);
    }

    ElMessage.success(dialogMode.value === "create" ? "添加成功" : "更新成功");
    editDialogVisible.value = false;
    fetchQuestions();
  } catch (error) {
    ElMessage.error(`保存失败: ${(error as Error).message}`);
  } finally {
    isSaving.value = false;
  }
};

// 删除题目
const deleteQuestion = async (id: number) => {
  ElMessageBox.confirm("确认删除该题目吗？此操作不可恢复。", "警告", {
    confirmButtonText: "确认",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/questions/${id}`,
          {
            method: "DELETE",
          },
        );

        if (!response.ok) {
          throw new Error("删除失败");
        }

        ElMessage.success("删除成功");
        fetchQuestions();
      } catch (error) {
        ElMessage.error("删除失败: " + (error as Error).message);
      }
    })
    .catch(() => {
      // 用户取消删除
    });
};

// 渲染Markdown
const renderMarkdown = (content: string) => {
  if (!content) return "";
  return md.render(content);
};

// 截取Markdown文本
const truncateMarkdown = (content: string, length: number) => {
  if (!content) return "";
  const plainText = content.replace(/[#*_[\]()`]/g, "").trim();
  return plainText.length > length
    ? plainText.substring(0, length) + "..."
    : plainText;
};

// 获取类型标签
const getTypeLabel = (type: string) => {
  switch (type) {
    case "comprehensive":
      return "综合知识";
    case "caseAnalysis":
      return "案例分析";
    case "thesis":
      return "论文题目";
    default:
      return type;
  }
};

// 获取类型标签样式
const getTypeTag = (type: string) => {
  switch (type) {
    case "comprehensive":
      return "primary";
    case "caseAnalysis":
      return "success";
    case "thesis":
      return "warning";
    default:
      return "info";
  }
};

// 分页事件处理
const handleSizeChange = (val: number) => {
  pagination.pageSize = val;
  fetchQuestions();
};

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val;
  fetchQuestions();
};

// 对话框关闭处理
const handleDialogClose = () => {
  resetCurrentQuestion();
};

// 组件挂载时获取数据
onMounted(() => {
  fetchQuestions();
});
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
