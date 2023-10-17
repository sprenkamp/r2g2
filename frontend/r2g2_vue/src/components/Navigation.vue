<!-- Navigation.vue -->

<template>
    <el-menu class="el-menu flex-container" mode="horizontal" :ellipsis="false">
        <el-menu-item index="0">LOGO</el-menu-item>
        <div class="flex-grow"/>
        <!-- <el-menu-item>
            <el-button color="FFFFFF" type="primary" class="button1">
                <router-link to="/testpage" class="test">test</router-link>
            </el-button>
        </el-menu-item> -->

        <router-link to="/" class="Home">
            <el-menu-item index="0.5">
                <el-icon><house /></el-icon>
                Home
            </el-menu-item>
        </router-link>

        <router-link to="/Telegram" class="Telegram">
            <el-menu-item index="2">
                <el-icon><list /></el-icon>
                Telegram
            </el-menu-item>
        </router-link>

        <!-- <router-link to="/Page3" class="Page3">
            <el-menu-item index="3">
                <el-icon><setting /></el-icon>
                Page 3
            </el-menu-item>
        </router-link> -->

        <el-switch 
            v-model='themeConfig.isDark'
            size="large"
            :active-action-icon="Moon"
            :inactive-action-icon="Sunny"
            style="--el-switch-on-color: #413c3c; --el-switch-off-color: gray;"
        />

        <el-menu-item index="5">
            <el-popover trigger="hover" placement="bottom" :width="170" :height="100">
                <el-button size="small" type="primary" plain @click="$changeLocale('English')">English</el-button>
                <el-button size="small" type="primary" plain @click="$changeLocale('Deutsch')">Deutsch</el-button>
                <template #reference>
                    <Icon icon="mdi:language" width="24" height="24" />
                </template>
            </el-popover>
        </el-menu-item>
    </el-menu>
</template>
  
<script setup>
import {reactive} from 'vue'
import {useDark} from "@vueuse/core";
import {
    House as house,
    Opportunity as opportunity,
    Menu as IconMenu,
    List as list,
    Setting,
    Sunny,
    Moon,
} from '@element-plus/icons-vue';
import {Icon} from '@iconify/vue'

const isDark = useDark();
const themeConfig = reactive({
  isDark: isDark,
});

</script>

<style scoped>
.flex-container {
    display: flex;
    align-items: center;
    background-color: transparent;
    backdrop-filter: blur(5px);
}
.flex-grow {
    flex-grow: 1;
}
</style>
