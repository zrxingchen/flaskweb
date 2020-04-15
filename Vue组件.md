## 一、组件

1. **组件是Vue项目中拥有自己作用域，数据，方法的特殊部分，项目中的组件可以重复使用**

2. **创建组件需要三步：**

   ```
   创建组件： var ItemsComponents = Vue.extend({ })
   
   注册组件：Vue.component('items-component',ItemsComponents)
   
   使用组件：<'items-component></'items-component>
   ```

   注意：Vue2.X规范的写法：

   ```
   Vue.component('items-component',{template:'<h1> Hello </h1>'})
   ```

3. **vue 中的组件**

   vue init webpack component-demo

   通过template 标签在HTML声明模板

   

4. **组件中的data和el属性**

   ```HTML
   <template id="hello">
     <h1>hello</h1>
   </template>
   //vue中要求用函数的形式来声明这些属性
   Vue.component("hello-component",{
     el:function(){
       return "#hello";
     },
     data:function(){
       return {
         msg:'hello'
    }
     }
   })
   ```
   
   

5. **组件的作用域（父子组件进行数据传递）**

   组件都有自己的独立的作用域，而且不会被其他组件访问到，但是，项目中全局作用域可以被所有注册过的组件访问。

   在组件内不能使用父作用域的数据，如果要是用父作用域的数据的话，指出到底哪个组件的父级数据属性可以被访问，

   - 通过props属性传递，
   - 用v-bind把他们绑定到组件上

6. **组件嵌套**

   

## 二、单文件组件（.vue）

1. 单文件组件，就是以.vue结尾的文件，使用vue-cli生成

2. 一个Vue单文件组件由3个部分组成：
   - template     HTML模板
   - script        JavaScript代码
   - style         CSS样式

3. 新建一个simple文件夹，cd simple ,  vue init webpack-simple，一路回车即可

4. 单文件组件，对style设置scoped属性就可以将css限制在本组件内

   

## 三、vue-router

插件    npm install vue-router --save

```
import VueRouter from 'vue-router'

Vue.use(VueRouter)
let router = new VueRouter({
  mode:history,
  routes:[
    {
      path:'/',
      component:IndexPage
    }
  ]
})

在new Vue（{
	router
}）
```





```
index.vue 模板


<template>
  <div class="index-wrapper">
    <div class="index-left">
      <!-- 全部产品 -->
      <div class="index-left-block">
        <h2>全部产品</h2>
        <h3>PC产品</h3>
        <ul>
          <li>大大大</li>
        </ul>
        <div class="hr"></div>
        <h3>手机应用类</h3>
        <ul>
          <li>大大大</li>
        </ul>
      </div>
      <!-- 最新消息 -->
      <div class="index-left-block lastest-news">
        <h2>最新消息</h2>
        <ul>
          <li>ddd</li>
        </ul>
      </div>
    </div>
    <div class="index-right">
      <div style="margin:0 auto;width:700px;height:300px;background:red;">将来使用组件代替</div>
      <div class="index-boader-list">
        <div class="index-boader-item">
          <h2>第1个</h2>
          <p>第1个商品描述</p>
          <div class="index-boader-button">立即购买</div>
        </div>
        <div class="index-boader-item">
          <h2>第2个</h2>
          <p>第2个商品描述</p>
          <div class="index-boader-button">立即购买</div>
        </div>
        <div class="index-boader-item">
          <h2>第3个</h2>
          <p>第3个商品描述</p>
          <div class="index-boader-button">立即购买</div>
        </div>
        <div class="index-boader-item">
          <h2>第4个</h2>
          <p>第4个商品描述</p>
          <div class="index-boader-button">立即购买</div>
        </div>
      </div>
    </div>
  </div>
</template>
```



```
index.vue 样式


<style scoped>
.index-wrapper {
  display: flex;
}
.index-left {
  width: 30%;
}
.index-right {
  width: 70%;
}
.index-left-block {
  margin: 15px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 1px #dddddd;
}
.index-left-block .hr {
  border-bottom: 1px solid black;
  margin: 20px 0;
}
.index-left-block h2 {
  background: #4fc08d;
  color: #ffffff;
  padding: 10px 15px;
  margin-bottom: 20px;
}
.index-left-block h3 {
  color: #222;
  font-weight: bolder;
  padding: 0 15px 5px 15px;
}
.index-left-block ul {
  padding: 10px 15px;
}
.index-left-block li {
  padding: 5px;
}
.index-boader-list {
  display: flex;
  flex-wrap: wrap;
  margin-top: 20px;
  justify-content: center;
}
.index-boader-item {
  width: 30%;
  height: 125px;
  padding-left: 120px;
  background: #ffffff;
  margin-right: 1%;
  box-shadow: 0 0 1px #ddd;
  margin-bottom: 20px;
  border-radius: 0 0 10px 10px;
}
</style>
```



```
index.vue  javascript


<script>
export default {
  data() {
    return {
      productList: {
        pc: {
          title: "PC产品",
          list: [
            {
              title: "数据统计",
              url: "http://starcraft.com"
            },
            {
              title: "数据预测",
              url: "http://warcraft.com"
            },
            {
              title: "流量分析",
              url: "http://overwatch.com",
              hot: true
            },
            {
              title: "广告发布",
              url: "http://hearstone.com"
            }
          ]
        },
        app: {
          title: "手机应用类",
          list: [
            {
              title: "91助手",
              url: "http://weixin.com"
            },
            {
              title: "产品助手",
              url: "http://weixin.com"
            },
            {
              title: "智能地图",
              url: "http://maps.com"
            },
            {
              title: "语音助手",
              url: "http://phone.com"
            }
          ]
        }
      }
    }
  }
};
</script>
```



```html
index.vue 数据绑定

<template v-for="product in productList">
          <h3>{{ product.title }}</h3>
          <ul>
            <li v-for="item in product.list">
                <a v-bind:href="item.url">{{ item.title }}</a>
            </li>
          </ul>
          <div class="hr"></div>
</template>
```











