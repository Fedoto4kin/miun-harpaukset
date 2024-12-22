<template>
  <div class="switch-button" :class="{ 'switch-on': isChecked }" @click="toggleSwitch">
    <span class="switch-label">{{ isChecked ? onLabel : offLabel }}</span>
    <div class="switch-toggle"></div>
  </div>
</template>

<script>
export default {
  name: 'SwitchButton',
  props: {
    onLabel: {
      type: String,
      default: 'On'
    },
    offLabel: {
      type: String,
      default: 'Off'
    },
    checked: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isChecked: this.checked
    };
  },
  methods: {
    toggleSwitch() {
      this.isChecked = !this.isChecked;
      this.$emit('change', this.isChecked);
    }
  }
};
</script>

<style scoped>
.switch-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 180px;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 25px;
  cursor: pointer;
  background-color: #f0f0f0;
}
.switch-button.switch-on {
  background-color: #ffc107;
}
.switch-label {
  flex-grow: 1;
  text-align: center;
  font-weight: bold;
}
.switch-toggle {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: white;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}
.switch-button.switch-on .switch-toggle {
  transform: translateX(150%);
}
</style>
