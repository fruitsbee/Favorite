let dashboardData = {};
const GAS_URL = "https://script.google.com/macros/s/AKfycbxUkzjpPeMgu_EFqM2ukvGGWiKclmP6xklXujQ5Yopc9nc2I7mtczLEyof0Iy0CMZRd/exec";

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

function initApp() {
    document.getElementById('game-container').style.display = 'flex';
    document.getElementById('add-btn-container').style.display = 'block';
    loadData();
    setupInteractJs();
}

function showLoading(show) {
    document.getElementById('loading-overlay').style.display = show ? 'flex' : 'none';
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    document.getElementById('toast-msg').innerText = msg;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 2000);
}

// ==== API COMMUNICATION ====
async function gasApiCall(payload) {
    if (!GAS_URL) throw new Error("API URL not set");

    if (payload.action === 'getData') {
        // We can use GET for getting data
        const res = await fetch(`${GAS_URL}?action=getData`);
        const json = await res.json();
        if (json.status !== "success") throw new Error(json.message);
        return json;
    }

    // Follow POST redirect (GAS web app POST needs careful handling for CORS, 
    // usually Content-Type: text/plain is safer to avoid Preflight errors)
    const res = await fetch(GAS_URL, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: JSON.stringify(payload)
    });

    const json = await res.json();
    if (json.status !== "success") throw new Error(json.message);
    return json;
}

function loadData() {
    showLoading(true);
    gasApiCall({ action: 'getData' })
        .then(res => {
            dashboardData = res.data;
            renderCalendar(res.data.calendar);
            renderTodos(res.data.todos);
            renderMemo(res.data.memo);
            renderBookmarks(res.data.bookmarks);
            showLoading(false);
        })
        .catch(err => {
            console.error(err);
            showLoading(false);
            alert('데이터를 가져오는데 실패했습니다. URL과 배포 설정을 확인해주세요.');
        });
}

// === RENDERERS ===
function renderCalendar(events) {
    const container = document.getElementById('calendar-list');
    container.innerHTML = '';

    if (!events || events.length === 0) {
        container.innerHTML = '<p>일정이 없습니다.</p>';
        return;
    }

    let todayDate = new Date().toISOString().split('T')[0];

    events.forEach(ev => {
        let div = document.createElement('div');
        div.className = 'calendar-item';

        let stDate = new Date(ev.startTimeStr);
        let ds = stDate.toLocaleDateString('ko-KR', { month: 'numeric', day: 'numeric', weekday: 'short' });
        let ts = ev.isAllDay ? '종일' : stDate.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' });

        if (ev.startTimeStr.startsWith(todayDate)) {
            div.classList.add('today');
            ds = '오늘';
        }

        div.innerHTML = `
      <div class="calendar-title">${ev.title}</div>
      <div class="calendar-time">${ds} ${ts}</div>
    `;
        container.appendChild(div);
    });
}

function renderTodos(todos) {
    const container = document.getElementById('todo-list');
    container.innerHTML = '';

    if (!todos || todos.length === 0) {
        container.innerHTML = '<p style="font-size:12px">할 일이 없습니다.</p>';
        return;
    }

    todos.forEach(todo => {
        let div = document.createElement('div');
        div.className = 'todo-item';

        let checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'nes-checkbox is-dark';
        checkbox.checked = todo.completed;
        checkbox.onchange = (e) => toggleTodoStatus(todo.id, e.target.checked);

        let label = document.createElement('label');

        let spanTxt = document.createElement('span');
        spanTxt.innerText = todo.task;

        label.appendChild(checkbox);
        label.appendChild(spanTxt);

        if (todo.completed) {
            spanTxt.style.textDecoration = 'line-through';
            spanTxt.style.color = '#888';
        }

        let delBtn = document.createElement('span');
        delBtn.className = 'delete-btn';
        delBtn.innerText = '×';
        delBtn.onclick = () => deleteTodoItem(todo.id, div);

        div.appendChild(label);
        div.appendChild(delBtn);

        container.appendChild(div);
    });
}

function renderMemo(memoText) {
    document.getElementById('memo-textarea').value = memoText || '';
}

function renderBookmarks(bookmarks) {
    const desktop = document.getElementById('desktop');
    desktop.innerHTML = '';

    if (!bookmarks) return;

    bookmarks.forEach(bm => {
        appendBookmarkElement(bm);
    });
}

function appendBookmarkElement(bm) {
    const desktop = document.getElementById('desktop');
    let div = document.createElement('div');
    div.className = 'draggable-asset';
    div.id = bm.id;

    // Load local storage states
    let localStateStr = localStorage.getItem('state_' + bm.id);
    let localState = localStateStr ? JSON.parse(localStateStr) : { locked: false, w: '', h: '' };

    
    // Use valid responsive percentages, default to center (50%) if invalid/huge pixel values
    let safeX = parseFloat(bm.x) || 50;
    let safeY = parseFloat(bm.y) || 50;
    if (safeX > 100 || safeX < -50) safeX = 50; // Legacy pixel cleanup
    if (safeY > 100 || safeY < -50) safeY = 50;
    
    // Position using percentages so they stick visually relative to the background
    div.style.left = safeX + '%';
    div.style.top = safeY + '%';
    div.style.transform = 'translate(-50%, -50%)'; // Center pivot
    
    div.setAttribute('data-px', safeX);
    div.setAttribute('data-py', safeY);


    if (localState.w && localState.h) {
        div.style.width = localState.w;
        div.style.height = localState.h;
    }

    if (localState.locked) {
        div.classList.add('locked');
    }

    div.ondblclick = () => window.open(bm.url, '_blank');

    let iconHtml = '';
    if (bm.icon && (bm.icon.startsWith('http') || bm.icon.startsWith('data:') || bm.icon.startsWith('assets/') || bm.icon.includes('.png') || bm.icon.includes('.gif'))) {
        iconHtml = `<img src="${bm.icon}" class="sprite-icon" draggable="false" style="width:100%; height:100%; object-fit:contain;">`;
    } else {
        iconHtml = `<div class="icon">${bm.icon || '💾'}</div>`;
    }

    div.innerHTML = `
      <div class="lock-asset" onclick="event.stopPropagation(); toggleLock('${bm.id}')">✔</div>
      <div class="delete-asset" onclick="event.stopPropagation(); deleteBookmarkAsset('${bm.id}')">×</div>
      ${iconHtml}
      <div class="label">${bm.title}</div>
    `;

    desktop.appendChild(div);
}

window.toggleLock = function (id) {
    let el = document.getElementById(id);
    if (!el) return;

    let isLocked = el.classList.contains('locked');
    if (isLocked) {
        el.classList.remove('locked');
    } else {
        el.classList.add('locked');
    }

    let localStateStr = localStorage.getItem('state_' + id);
    let localState = localStateStr ? JSON.parse(localStateStr) : { w: el.style.width, h: el.style.height };
    localState.locked = !isLocked;
    localStorage.setItem('state_' + id, JSON.stringify(localState));
};

// === INTERACT.JS CONFIG ===
function setupInteractJs() {
    interact('.draggable-asset')
        .draggable({
            inertia: true,
            modifiers: [
                interact.modifiers.restrictRect({
                    restriction: 'parent',
                    endOnly: true
                })
            ],
            autoScroll: false,
            filter: function (event) {
                // Prevent dragging if element or its parent is locked
                return !event.target.closest('.locked');
            },
            listeners: {
                move: dragMoveListener,
                end: (event) => {
                    let target = event.target;
                    let x = parseFloat(target.getAttribute('data-px')) || 50;
                    let y = parseFloat(target.getAttribute('data-py')) || 50;
                    // Round percentages to 2 decimal places to save space
                    x = Math.round(x * 100) / 100;
                    y = Math.round(y * 100) / 100;
                    let id = target.id;

                    gasApiCall({ action: 'saveBookmarkPosition', id: id, x: x, y: y })
                        .catch(console.error);
                }
            }
        })
        .resizable({
            edges: { left: false, right: true, bottom: true, top: false },
            listeners: {
                move: function (event) {
                    let target = event.target;
                    // Prevent resizing if locked
                    if (target.classList.contains('locked')) return;

                    let x = parseFloat(target.getAttribute('data-px')) || 50;
                    let y = parseFloat(target.getAttribute('data-py')) || 50;
                    // Round percentages to 2 decimal places to save space
                    x = Math.round(x * 100) / 100;
                    y = Math.round(y * 100) / 100;

                    let newW = event.rect.width + 'px';
                    let newH = event.rect.height + 'px';
                    Object.assign(target.style, {
                        width: newW,
                        height: newH,
                        transform: `translate(${x}px, ${y}px)`
                    });
                },
                end: function (event) {
                    let target = event.target;
                    if (target.classList.contains('locked')) return;
                    let localStateStr = localStorage.getItem('state_' + target.id);
                    let localState = localStateStr ? JSON.parse(localStateStr) : { locked: false };
                    localState.w = target.style.width;
                    localState.h = target.style.height;
                    localStorage.setItem('state_' + target.id, JSON.stringify(localState));
                }
            }
        });
}

function dragMoveListener(event) {
    let target = event.target;
    if (target.classList.contains('locked')) return;
    
    let parent = target.parentElement.getBoundingClientRect();
    
    // Get current percent values
    let currentPX = parseFloat(target.getAttribute('data-px')) || 50;
    let currentPY = parseFloat(target.getAttribute('data-py')) || 50;
    
    // Add pixel movement converted to percentage of parent bounds
    let newPX = currentPX + (event.dx / parent.width) * 100;
    let newPY = currentPY + (event.dy / parent.height) * 100;
    
    // Apply new percentage
    target.style.left = newPX + '%';
    target.style.top = newPY + '%';
    
    // Update attribute cache
    target.setAttribute('data-px', newPX);
    target.setAttribute('data-py', newPY);
}

// === SPRITE SELECTION ===
window.selectSprite = function (element, url) {
    // Remove selected class from all
    document.querySelectorAll('.preset-sprite').forEach(el => el.classList.remove('selected'));
    // Add to clicked
    element.classList.add('selected');
    // Set hidden input value
    document.getElementById('bm-icon').value = url;
};

// === MUTATION ACTIONS ===
window.addTodoItem = function () {
    let input = document.getElementById('todo-input');
    let text = input.value.trim();
    if (!text) return;

    input.value = '';

    // Optimistic
    let td = { id: 'temp', task: text, completed: false };
    if (!dashboardData.todos) dashboardData.todos = [];
    dashboardData.todos.push(td);
    renderTodos(dashboardData.todos);

    gasApiCall({ action: 'addTodo', task: text })
        .then(res => {
            let idx = dashboardData.todos.findIndex(t => t.id === 'temp');
            if (idx >= 0) dashboardData.todos[idx] = res.result;
            renderTodos(dashboardData.todos);
        })
        .catch(console.error);
};

window.toggleTodoStatus = function (id, isCompleted) {
    let td = dashboardData.todos.find(t => t.id === id);
    if (td) td.completed = isCompleted;
    renderTodos(dashboardData.todos);

    gasApiCall({ action: 'toggleTodo', id: id, completed: isCompleted })
        .catch(console.error);
};

window.deleteTodoItem = function (id, elem) {
    dashboardData.todos = dashboardData.todos.filter(t => t.id !== id);
    elem.remove();

    gasApiCall({ action: 'deleteTodo', id: id })
        .catch(console.error);
};

let memoTimeout;
window.debouncedMemoSave = function () {
    clearTimeout(memoTimeout);
    let val = document.getElementById('memo-textarea').value;
    memoTimeout = setTimeout(() => {
        gasApiCall({ action: 'updateMemo', content: val })
            .then(() => showToast('메모 저장됨'))
            .catch(console.error);
    }, 1000);
};

window.saveNewBookmark = function (e) {
    e.preventDefault();
    let title = document.getElementById('bm-title').value;
    let url = document.getElementById('bm-url').value;
    let icon = document.getElementById('bm-icon').value || '💾';

    if (!url.startsWith('http')) url = 'https://' + url;

    let x = 50;
    let y = 50; // Percentages

    document.getElementById('add-bookmark-modal').close();

    gasApiCall({ action: 'addBookmark', title: title, url: url, icon: icon, x: x, y: y })
        .then(res => {
            if (!dashboardData.bookmarks) dashboardData.bookmarks = [];
            let newBm = { id: res.result, title: title, url: url, icon: icon, x: x, y: y };
            dashboardData.bookmarks.push(newBm);
            appendBookmarkElement(newBm);
            showToast('에셋 추가됨');
        })
        .catch(console.error);

    document.getElementById('bm-title').value = '';
    document.getElementById('bm-url').value = '';

    // reset to first sprite
    let firstSprite = document.querySelector('.preset-sprite');
    if (firstSprite) {
        window.selectSprite(firstSprite, 'assets/sprite_0.png');
    }
};

window.deleteBookmarkAsset = function (id) {
    if (confirm('이 에셋을 삭제하시겠습니까?')) {
        document.getElementById(id).remove();
        dashboardData.bookmarks = dashboardData.bookmarks.filter(b => b.id !== id);
        gasApiCall({ action: 'deleteBookmark', id: id })
            .catch(console.error);
    }
};

// === MOBILE MENU ===
window.toggleMobileMenu = function() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
};
