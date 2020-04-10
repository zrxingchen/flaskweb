<template>
  <div id="app">
    <h2>我的购物车清单</h2>
    <div class="input-group">
      <input class="js-new-item form-control" type="text" placeholder="输入你想购买的物品" />
      <span class="input-group-btn">
        <button type="button" class="js-add btn btn-default">添加到购物车</button>
      </span>
    </div>
    <!-- 购物车列表 -->
    <ul>
      <li>
        <div class="checkbox">
          <label for>
            <input class="js-item" type="checkbox" /> 苹果
          </label>
        </div>
      </li>
      <li>
        <div class="checkbox">
          <label for>
            <input class="js-item" type="checkbox" /> 香蕉
          </label>
        </div>
      </li>
      <li>
        <div class="checkbox">
          <label for>
            <input class="js-item" type="checkbox" /> 电脑
          </label>
        </div>
      </li>
    </ul>

    <!-- 修改标题 -->
    <div class="footer">
      <hr />
      <span>改变你的标题</span>
      <input type="text" class="js-change-title" value="我的购物车清单" />
    </div>
  </div>
</template>

<script>
</script>

<style>
.container {
  width: 40%;
  margin: 100px auto;
}
.removed {
  color: gray;
}
.removed label {
  text-decoration: line-through;
}
ul {
  border: 1px solid black;
  margin-top: 30px;
}
ul li {
  list-style: none;
}
