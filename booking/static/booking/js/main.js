document.querySelectorAll('[data-slider]').forEach((slider) => {
  const slides = [...slider.querySelectorAll('.slide')];
  if (!slides.length) return;

  let current = 0;
  const show = (nextIndex) => {
    slides[current].classList.remove('active');
    current = (nextIndex + slides.length) % slides.length;
    slides[current].classList.add('active');
  };

  let timer = setInterval(() => show(current + 1), 3000);
  const restart = () => {
    clearInterval(timer);
    timer = setInterval(() => show(current + 1), 3000);
  };

  slider.querySelector('[data-next]')?.addEventListener('click', () => {
    show(current + 1);
    restart();
  });

  slider.querySelector('[data-prev]')?.addEventListener('click', () => {
    show(current - 1);
    restart();
  });
});

document.querySelectorAll('[data-alert]').forEach((btn) => {
  btn.addEventListener('click', () => alert(btn.dataset.alert));
});

const validators = {
  username(value) {
    if (!value) return 'Введите логин.';
    if (value.length < 6) return 'Минимум 6 символов.';
    if (!/^[A-Za-z0-9]+$/.test(value)) return 'Только латинские буквы и цифры.';
    if (!/[A-Za-z]/.test(value) || !/\d/.test(value)) return 'Нужны и буквы, и цифры.';
    return '';
  },
  password(value) {
    if (!value) return 'Введите пароль.';
    if (value.length < 8) return 'Минимум 8 символов.';
    return '';
  },
  full_name(value) {
    if (!value.trim()) return 'Введите ФИО.';
    if (value.trim().split(/\s+/).length < 2) return 'Укажите фамилию и имя.';
    return '';
  },
  phone(value) {
    const digits = value.replace(/\D/g, '');
    if (!digits || digits === '7') return 'Введите номер телефона.';
    if (digits.length < 11) return 'Номер должен содержать 11 цифр.';
    if (!digits.startsWith('7')) return 'Номер должен начинаться с +7.';
    return '';
  },
  email(value) {
    if (!value) return 'Введите e-mail.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Проверьте формат e-mail.';
    return '';
  },
};

function setValidationState(input) {
  const rule = input.dataset.rule;
  if (!rule || !validators[rule]) return;

  let hint = input.parentElement.querySelector('.live-hint');
  if (!hint) {
    hint = document.createElement('small');
    hint.className = 'live-hint';
    input.insertAdjacentElement('afterend', hint);
  }

  const message = validators[rule](input.value);
  hint.textContent = message || 'Заполнено верно.';
  hint.classList.toggle('ok', !message);
  input.classList.toggle('invalid', Boolean(message));
  input.classList.toggle('valid', !message && input.value.length > 0);
}

function formatPhone(value) {
  let digits = value.replace(/\D/g, '');
  if (!digits) return '+7 ';
  if (digits[0] === '8') digits = '7' + digits.slice(1);
  if (digits[0] !== '7') digits = '7' + digits;
  digits = digits.slice(0, 11);

  const parts = ['+7'];
  if (digits.length > 1) parts.push(' (' + digits.slice(1, 4));
  if (digits.length >= 4) parts[1] += ')';
  if (digits.length > 4) parts.push(' ' + digits.slice(4, 7));
  if (digits.length > 7) parts.push('-' + digits.slice(7, 9));
  if (digits.length > 9) parts.push('-' + digits.slice(9, 11));
  return parts.join('');
}

document.querySelectorAll('[data-phone-mask]').forEach((input) => {
  input.addEventListener('focus', () => {
    if (!input.value) input.value = '+7 ';
  });
  input.addEventListener('input', () => {
    input.value = formatPhone(input.value);
    setValidationState(input);
  });
});

document.querySelectorAll('[data-rule]').forEach((input) => {
  input.addEventListener('input', () => setValidationState(input));
  input.addEventListener('blur', () => setValidationState(input));
  if (input.value) setValidationState(input);
});
