<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex gap-6">
        <!-- 答题区域 -->
        <div class="flex-1">
          <!-- 题目内容 -->
          <div v-if="currentQuestion" class="border rounded-lg p-6 mb-6">
            <div class="flex justify-between items-center mb-4">
              <div class="flex gap-2">
                <el-tag type="primary">
                  {{ getTypeLabel(currentQuestion.type) }}
                </el-tag>
                <el-tag type="success">
                  {{ currentQuestion.source }}
                </el-tag>
                <el-tag type="warning">
                  {{ currentQuestion.domain }}
                </el-tag>
              </div>

              <div>
                {{ answeredCount }}/大题数{{ questions.length }}/总题数{{
                  totalQuestions
                }}
              </div>
            </div>

            <!-- 题干 -->
            <div class="mb-6">
              <h3 class="text-lg font-semibold mb-2">题干</h3>
              <div
                class="p-4 bg-gray-50 rounded"
                v-html="renderMarkdown(currentQuestion.stem)"
              ></div>
            </div>

            <!-- 不同题型的答题区域 -->
            <div v-if="currentQuestion.type === 'comprehensive'">
              <h3 class="text-lg font-semibold mb-4">选择题部分</h3>

              <div
                v-for="(choice, index) in currentQuestion.choices"
                :key="index"
                class="mb-6 p-4 border rounded"
              >
                <h4 class="font-medium mb-3">第{{ index + 1 }}题：</h4>

                <div class="space-y-2">
                  <div
                    v-for="(option, optIndex) in choice.options"
                    :key="optIndex"
                    class="flex items-start p-3 rounded border cursor-pointer hover:bg-gray-50"
                    :class="{
                      'bg-blue-50 border-blue-300': isOptionSelected(
                        currentQuestionIndex,
                        index,
                        optIndex,
                      ),
                      'border-gray-200': !isOptionSelected(
                        currentQuestionIndex,
                        index,
                        optIndex,
                      ),
                    }"
                    @click="selectOption(currentQuestionIndex, index, optIndex)"
                  >
                    <el-radio
                      :model-value="
                        isOptionSelected(currentQuestionIndex, index, optIndex)
                      "
                      :value="true"
                      class="mr-2 mt-1"
                    ></el-radio>
                    <span class="font-medium mr-2 flex-shrink-0">
                      {{ String.fromCharCode(65 + optIndex) }}.
                    </span>
                    <span
                      v-html="renderMarkdown(option.text)"
                      class="flex-grow"
                    ></span>
                  </div>
                </div>
              </div>
            </div>

            <div v-else-if="currentQuestion.type === 'caseAnalysis'">
              <h3 class="text-lg font-semibold mb-4">问题部分</h3>

              <div
                v-for="(subQuestion, index) in currentQuestion.subQuestions"
                :key="index"
                class="mb-6 p-4 border rounded"
              >
                <h4 class="font-medium mb-3">
                  问题{{ index + 1 }}：{{ subQuestion.question }}
                </h4>

                <el-input
                  type="textarea"
                  :rows="4"
                  placeholder="请输入您的答案..."
                  :model-value="getSubAnswer(currentQuestionIndex, index)"
                  @update:model-value="
                    (val: string) =>
                      setSubAnswer(currentQuestionIndex, index, val)
                  "
                ></el-input>
              </div>
            </div>

            <div v-else-if="currentQuestion.type === 'thesis'">
              <h3 class="text-lg font-semibold mb-2">论文写作</h3>
              <el-input
                type="textarea"
                :rows="10"
                placeholder="请输入您的论文答案..."
                :model-value="getEssayAnswer(currentQuestionIndex)"
                @update:model-value="
                  (val: string) => setEssayAnswer(currentQuestionIndex, val)
                "
              ></el-input>
            </div>
          </div>
        </div>

        <!-- 答题卡区域 -->
        <div class="w-80">
          <div class="border rounded-lg p-4 sticky top-6">
            <div class="text-lg">
              <span class="font-semibold">答题耗时:</span>
              <span class="text-red-600 ml-2">{{
                formatTime(elapsedTime)
              }}</span>
            </div>

            <div class="mb-6 pb-4 pt-4 border-b">
              <!-- 导航按钮 -->
              <div class="flex justify-between">
                <el-button @click="endExam" type="danger">结束</el-button>
                <el-button
                  @click="prevQuestion"
                  :disabled="currentQuestionIndex === 0"
                  type="primary"
                  plain
                >
                  上一题
                </el-button>
                <el-button
                  @click="nextQuestion"
                  :disabled="currentQuestionIndex === questions.length - 1"
                  type="primary"
                >
                  下一题
                </el-button>
              </div>
            </div>

            <div class="grid grid-cols-5 gap-2">
              <template v-for="(question, index) in questions" :key="index">
                <div
                  v-if="
                    question.type !== 'comprehensive' &&
                    question.type !== 'caseAnalysis'
                  "
                  class="flex items-center justify-center h-10 w-10 rounded cursor-pointer border"
                  :class="{
                    'bg-blue-500 text-white': index === currentQuestionIndex,
                    'bg-blue-100 text-blue-800': isQuestionAnswered(index),
                    'bg-white text-gray-800':
                      !isQuestionAnswered(index) &&
                      index !== currentQuestionIndex,
                  }"
                  @click="jumpToQuestion(index)"
                >
                  {{ index + 1 }}
                </div>

                <template v-else>
                  <template v-if="getSubQuestionCount(question) === 1">
                    <!-- 只有一个子题时，不显示小题号 -->
                    <div
                      class="flex items-center justify-center h-10 w-10 rounded cursor-pointer border"
                      :class="{
                        'bg-blue-500 text-white':
                          index === currentQuestionIndex,
                        'bg-blue-100 text-blue-800': isQuestionAnswered(index),
                        'bg-white text-gray-800':
                          !isQuestionAnswered(index) &&
                          index !== currentQuestionIndex,
                      }"
                      @click="jumpToQuestion(index)"
                    >
                      {{ index + 1 }}
                    </div>
                  </template>
                  <template v-else>
                    <!-- 多个子题时，显示小题号 -->
                    <div
                      v-for="(_subQuestion, subIndex) in getSubQuestionCount(
                        question,
                      )"
                      :key="`${index}-${subIndex}`"
                      class="flex items-center justify-center h-10 w-10 rounded cursor-pointer border text-xs"
                      :class="{
                        'bg-blue-500 text-white': isSubQuestionCurrent(
                          index,
                          subIndex,
                        ),
                        'bg-blue-100 text-blue-800': isSubQuestionAnswered(
                          index,
                          subIndex,
                        ),
                        'bg-white text-gray-800':
                          !isSubQuestionAnswered(index, subIndex) &&
                          !isSubQuestionCurrent(index, subIndex),
                      }"
                      @click="jumpToSubQuestion(index, subIndex)"
                    >
                      {{ index + 1 }}-{{ subIndex + 1 }}
                    </div>
                  </template>
                </template>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import MarkdownIt from "markdown-it";
import { useRouter } from "vue-router";

// 定义接口
interface Choice {
  options: { text: string }[];
  correctAnswer: number;
}

interface SubQuestion {
  question: string;
  answer: string;
  analysis: string;
}

interface QuestionData {
  id: number;
  type: "comprehensive" | "caseAnalysis" | "thesis";
  stem: string;
  source: string;
  domain: string;
  choices: Choice[];
  subQuestions: SubQuestion[];
  analysis: string;
}

interface AnswerData {
  selectedChoices: Record<number, number>; // 记录每道选择题的选项
  subAnswers: string[]; // 记录每道子题的答案
  essayAnswer: string; // 记录论文题答案
}

// 初始化Markdown解析器
const md = new MarkdownIt();
const router = useRouter();

// 状态变量
const questions = ref<QuestionData[]>([]);
const answers = ref<AnswerData[]>([]);
const currentQuestionIndex = ref(0);
const loading = ref(false);
const startTime = ref<number>(Date.now());
const elapsedTime = ref(0);
const timer = ref<number | null>(null);

// 计算属性
const currentQuestion = computed(
  () => questions.value[currentQuestionIndex.value],
);

const totalQuestions = computed(() => {
  let count = 0;
  questions.value.forEach((q) => {
    if (q.type === "comprehensive") {
      count += q.choices.length;
    } else if (q.type === "caseAnalysis") {
      count += q.subQuestions.length;
    } else {
      count += 1;
    }
  });
  return count;
});

const answeredCount = computed(() => {
  let count = 0;
  answers.value.forEach((answer, qIndex) => {
    const question = questions.value[qIndex];
    if (!answer || !question) return false;

    if (question.type === "comprehensive") {
      // 每个选择题都需要作答
      Object.keys(answer.selectedChoices).forEach((choiceIndex) => {
        if (answer.selectedChoices[parseInt(choiceIndex)] !== undefined) {
          count++;
        }
      });
    } else if (question.type === "caseAnalysis") {
      // 每个子问题都需要作答
      answer.subAnswers.forEach((subAnswer) => {
        if (subAnswer && subAnswer.trim()) {
          count++;
        }
      });
    } else {
      // 论文题只需要一个答案
      if (answer.essayAnswer && answer.essayAnswer.trim()) {
        count++;
      }
    }
  });
  return count;
});

// 检查题目是否已答
const isQuestionAnswered = (qIndex: number): boolean => {
  const answer = answers.value[qIndex];
  const question = questions.value[qIndex];

  // 提前判断 question 和 answer 是否存在
  if (!answer || !question) return false;

  if (question.type === "comprehensive") {
    // 所有选择题都已作答
    return question.choices.every(
      (_, choiceIndex) => answer.selectedChoices[choiceIndex] !== undefined,
    );
  } else if (question.type === "caseAnalysis") {
    // 所有子问题都已作答
    return question.subQuestions.every(
      (_, subIndex) =>
        answer.subAnswers[subIndex] && answer.subAnswers[subIndex].trim(),
    );
  } else {
    // 论文题已作答
    return !!answer.essayAnswer && answer.essayAnswer.trim() !== "";
  }
};

// 获取子题数量
const getSubQuestionCount = (question: QuestionData) => {
  if (question.type === "comprehensive") {
    return question.choices.length;
  } else if (question.type === "caseAnalysis") {
    return question.subQuestions.length;
  }
  return 1;
};

// 判断子题是否为当前题
const isSubQuestionCurrent = (qIndex: number, subIndex: number) => {
  return currentQuestionIndex.value === qIndex; // 简化处理，实际可根据需要细化
};

// 判断子题是否已回答
const isSubQuestionAnswered = (qIndex: number, subIndex: number) => {
  const answer = answers.value[qIndex];
  const question = questions.value[qIndex];

  if (!answer || !question) return false;

  if (question.type === "comprehensive") {
    return answer.selectedChoices[subIndex] !== undefined;
  } else if (question.type === "caseAnalysis") {
    return answer.subAnswers[subIndex] && answer.subAnswers[subIndex].trim();
  }
  return !!answer.essayAnswer && answer.essayAnswer.trim() !== "";
};

// 跳转到子题
const jumpToSubQuestion = (qIndex: number, subIndex: number) => {
  // 实现跳转逻辑，根据实际需求调整
  currentQuestionIndex.value = qIndex;
  // 可能还需要记录当前子题索引
};

// 检查选项是否被选中
const isOptionSelected = (
  qIndex: number,
  choiceIndex: number,
  optIndex: number,
): boolean => {
  return answers.value[qIndex]?.selectedChoices[choiceIndex] === optIndex;
};

// 获取题目类型标签
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

// 渲染Markdown
const renderMarkdown = (content: string) => {
  if (!content) return "";
  return md.render(content);
};

// 选择选项
const selectOption = (
  qIndex: number,
  choiceIndex: number,
  optIndex: number,
) => {
  if (!answers.value[qIndex]) {
    initAnswer(qIndex);
  }

  // 使用空值合并赋默认值，防止 undefined 访问
  const answer = answers.value[qIndex];
  if (answer) {
    answer.selectedChoices = answer.selectedChoices ?? {};
    answer.selectedChoices[choiceIndex] = optIndex;
  }
};

// 获取子问题答案
const getSubAnswer = (qIndex: number, subIndex: number): string => {
  return answers.value[qIndex]?.subAnswers[subIndex] ?? "";
};

// 设置子问题答案
const setSubAnswer = (qIndex: number, subIndex: number, value: string) => {
  if (!answers.value[qIndex]) {
    initAnswer(qIndex);
  }
  // 确保 answers.value[qIndex] 存在后再访问 subAnswers
  const answer = answers.value[qIndex];
  if (answer && !answer.subAnswers) {
    const question = questions.value[qIndex];
    answer.subAnswers = Array(question?.subQuestions?.length ?? 0).fill("");
  }
  if (answer) {
    answer.subAnswers[subIndex] = value;
  }
};

// 获取论文答案
const getEssayAnswer = (qIndex: number): string => {
  return answers.value[qIndex]?.essayAnswer ?? "";
};

// 设置论文答案
const setEssayAnswer = (qIndex: number, value: string) => {
  if (!answers.value[qIndex]) {
    initAnswer(qIndex);
  }
  if (answers.value[qIndex]) {
    answers.value[qIndex].essayAnswer = value;
  }
};

// 初始化答题数据
const initAnswer = (qIndex: number) => {
  const question = questions.value[qIndex];
  if (!answers.value[qIndex]) {
    answers.value[qIndex] = {
      selectedChoices: {},
      subAnswers: Array(question?.subQuestions?.length ?? 0).fill(""),
      essayAnswer: "",
    };
  } else {
    // 补充初始化逻辑以防部分字段缺失
    answers.value[qIndex].subAnswers =
      answers.value[qIndex].subAnswers ||
      Array(question?.subQuestions?.length ?? 0).fill("");
    answers.value[qIndex].selectedChoices =
      answers.value[qIndex].selectedChoices || {};
    answers.value[qIndex].essayAnswer = answers.value[qIndex].essayAnswer || "";
  }
};

// 跳转到指定题目
const jumpToQuestion = (index: number) => {
  currentQuestionIndex.value = index;
};

// 上一题
const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
  }
};

// 下一题
const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++;
  }
};

// 结束考试
const endExam = () => {
  ElMessageBox.confirm(
    "确定要结束考试并提交答案吗？结束后将无法修改答案。",
    "结束考试",
    {
      confirmButtonText: "确定提交",
      cancelButtonText: "继续答题",
      type: "warning",
    },
  )
    .then(() => {
      // 这里可以发送答案到服务器
      ElMessage.success("考试已提交");
      router.push("/results"); // 跳转到结果页面
    })
    .catch(() => {
      // 用户取消
    });
};

// 格式化时间
const formatTime = (milliseconds: number) => {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  if (hours > 0) {
    return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  }
  return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
};

// 获取题目数据
const fetchQuestions = async () => {
  loading.value = true;
  try {
    const response = await fetch("http://localhost:8000/api/questions");

    if (!response.ok) {
      throw new Error("获取试题失败");
    }

    const data = await response.json();
    questions.value = data.items || data;

    // 初始化答案数组
    answers.value = Array(questions.value.length)
      .fill(null)
      .map(() => ({
        selectedChoices: {},
        subAnswers: [],
        essayAnswer: "",
      }));

    // 初始化每个题目的子答案数组
    questions.value.forEach((question, index) => {
      if (!answers.value[index]) {
        answers.value[index] = {
          selectedChoices: {},
          subAnswers: [],
          essayAnswer: "",
        };
      }

      if (question.type === "caseAnalysis") {
        answers.value[index].subAnswers = Array(
          question.subQuestions.length,
        ).fill("");
      }
    });
  } catch (error) {
    ElMessage.error("获取题目失败: " + (error as Error).message);
  } finally {
    loading.value = false;
  }
};

// 更新计时器
const updateTimer = () => {
  elapsedTime.value = Date.now() - startTime.value;
};

// 组件挂载时
onMounted(() => {
  fetchQuestions();
  timer.value = window.setInterval(updateTimer, 1000);
});

// 组件卸载前
onBeforeUnmount(() => {
  if (timer.value) {
    clearInterval(timer.value);
  }
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
