const input = document.querySelector("input[name='shooting']");
const label = document.querySelector("label[name='shooting']");

input.addEventListener("input", event => {
  const value = Number(input.value) / 100;
  input.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label.innerHTML = Math.round(value * 100);
});

const input2 = document.querySelector("input[name='tackling']");
const label2 = document.querySelector("label[name='tackling']");

input2.addEventListener("input", event => {
  const value = Number(input2.value) / 100;
  input2.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label2.innerHTML = Math.round(value * 100);
});


const input3 = document.querySelector("input[name='crossing']");
const label3 = document.querySelector("label[name='crossing']");

input3.addEventListener("input", event => {
  const value = Number(input3.value) / 100;
  input3.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label3.innerHTML = Math.round(value * 100);
});

const input4 = document.querySelector("input[name='intercepting']");
const label4 = document.querySelector("label[name='intercepting']");

input4.addEventListener("input", event => {
  const value = Number(input4.value) / 100;
  input4.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label4.innerHTML = Math.round(value * 100);
});

const input5 = document.querySelector("input[name='aggressive']");
const label5 = document.querySelector("label[name='aggressive']");

input5.addEventListener("input", event => {
  const value = Number(input5.value) / 100;
  input5.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label5.innerHTML = Math.round(value * 100);
});

const input6 = document.querySelector("input[name='impulse']");
const label6 = document.querySelector("label[name='impulse']");

input6.addEventListener("input", event => {
  const value = Number(input6.value) / 100;
  input6.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label6.innerHTML = Math.round(value * 100);
});

const input7 = document.querySelector("input[name='assisting']");
const label7 = document.querySelector("label[name='assisting']");

input7.addEventListener("input", event => {
  const value = Number(input7.value) / 100;
  input7.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label7.innerHTML = Math.round(value * 100);
});

const input8 = document.querySelector("input[name='power']");
const label8 = document.querySelector("label[name='power']");

input8.addEventListener("input", event => {
  const value = Number(input8.value) / 100;
  input8.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label8.innerHTML = Math.round(value * 100);
});

const input9 = document.querySelector("input[name='height']");
const label9 = document.querySelector("label[name='height']");

input9.addEventListener("input", event => {
  const value = Number(input9.value) / 100;
  input9.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label9.innerHTML = Math.round(value * 100);
});