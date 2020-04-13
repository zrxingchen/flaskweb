export default{
    install:function(Vue){
         // 自定义指令square ，v-square
        Vue.directive('square',function(el,binding){
            el.innerHTML = Math.pow(binding.value,2)
    });
        Vue.directive('sqrt',function(el,binding){
            el.innerHTML = Math.sqrt(binding.value)
    })
    }
}