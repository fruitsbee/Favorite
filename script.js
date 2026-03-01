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
        let div = document.createElement('div');
        div.className = 'draggable-asset';
        div.id = bm.id;
        div.setAttribute('data-x', bm.x || 0);
        div.setAttribute('data-y', bm.y || 0);
        div.style.transform = `translate(${bm.x || 0}px, ${bm.y || 0}px)`;
        div.ondblclick = () => window.open(bm.url, '_blank');
        let iconHtml = '';
        if (bm.icon && (bm.icon.startsWith('http') || bm.icon.startsWith('data:') || bm.icon.startsWith('assets/') || bm.icon.includes('.png') || bm.icon.includes('.gif'))) {
            iconHtml = `<img src="${bm.icon}" class="sprite-icon" draggable="false">`;
        } else {
            iconHtml = `<div class="icon">${bm.icon || '💾'}</div>`;
        }
        div.innerHTML = `
      <div class="delete-asset" onclick="event.stopPropagation(); deleteBookmarkAsset('${bm.id}')">×</div>
      ${iconHtml}
      <div class="label">${bm.title}</div>
    `;
        desktop.appendChild(div);
    });
}
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
            listeners: {
                move: dragMoveListener,
                end: (event) => {
                    let target = event.target;
                    let x = parseFloat(target.getAttribute('data-x')) || 0;
                    let y = parseFloat(target.getAttribute('data-y')) || 0;
                    let id = target.id;
                    gasApiCall({ action: 'saveBookmarkPosition', id: id, x: x, y: y })
                        .catch(console.error);
                }
            }
        });
}
function dragMoveListener(event) {
    var target = event.target
    var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
    var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy
    target.style.transform = `translate(${x}px, ${y}px)`
    target.setAttribute('data-x', x)
    target.setAttribute('data-y', y)
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
    let y = 50;
    document.getElementById('add-bookmark-modal').close();
    gasApiCall({ action: 'addBookmark', title: title, url: url, icon: icon, x: x, y: y })
        .then(res => {
            if (!dashboardData.bookmarks) dashboardData.bookmarks = [];
            dashboardData.bookmarks.push({ id: res.result, title: title, url: url, icon: icon, x: x, y: y });
            renderBookmarks(dashboardData.bookmarks);
            showToast('에셋 추가됨');
        })
        .catch(console.error);
    document.getElementById('bm-title').value = '';
    document.getElementById('bm-url').value = '';
    // reset to first sprite
    let firstSprite = document.querySelector('.preset-sprite');
    if (firstSprite) {
        window.selectSprite(firstSprite, 'data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMTYgMTYiIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB4PSIxNCIgeT0iMCIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjEzIiB5PSIxIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iMTQiIHk9IjEiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNjYmNiY2IiLz48cmVjdCB4PSIxNSIgeT0iMSIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjEyIiB5PSIyIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iMTMiIHk9IjIiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNjYmNiY2IiLz48cmVjdCB4PSIxNCIgeT0iMiIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjExIiB5PSIzIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iMTIiIHk9IjMiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNjYmNiY2IiLz48cmVjdCB4PSIxMyIgeT0iMyIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjEwIiB5PSI0IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iMTEiIHk9IjQiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNjYmNiY2IiLz48cmVjdCB4PSIxMiIgeT0iNCIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjIiIHk9IjUiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSIzIiB5PSI1IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iOSIgeT0iNSIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjEwIiB5PSI1IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjY2JjYmNiIi8+PHJlY3QgeD0iMTEiIHk9IjUiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSIxIiB5PSI2IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iMiIgeT0iNiIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzhmNTYzYiIvPjxyZWN0IHg9IjMiIHk9IjYiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiM4ZjU2M2IiLz48cmVjdCB4PSI0IiB5PSI2IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iOCIgeT0iNiIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjkiIHk9IjYiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNjYmNiY2IiLz48cmVjdCB4PSIxMCIgeT0iNiIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjAiIHk9IjciIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSIxIiB5PSI3IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjZmJmMjM2Ii8+PHJlY3QgeD0iMiIgeT0iNyIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzhmNTYzYiIvPjxyZWN0IHg9IjMiIHk9IjciIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiM4ZjU2M2IiLz48cmVjdCB4PSI0IiB5PSI3IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjZmJmMjM2Ii8+PHJlY3QgeD0iNSIgeT0iNyIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjciIHk9IjciIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSI4IiB5PSI3IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjY2JjYmNiIi8+PHJlY3QgeD0iOSIgeT0iNyIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjEiIHk9IjgiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSIyIiB5PSI4IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjOGY1NjNiIi8+PHJlY3QgeD0iMyIgeT0iOCIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzhmNTYzYiIvPjxyZWN0IHg9IjQiIHk9IjgiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSI1IiB5PSI4IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iNiIgeT0iOCIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjciIHk9IjgiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNjYmNiY2IiLz48cmVjdCB4PSI4IiB5PSI4IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iMiIgeT0iOSIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjMiIHk9IjkiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSI1IiB5PSI5IiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwMDAwIi8+PHJlY3QgeD0iNiIgeT0iOSIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iI2NiY2JjYiIvPjxyZWN0IHg9IjciIHk9IjkiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSI0IiB5PSIxMCIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjxyZWN0IHg9IjUiIHk9IjEwIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjY2JjYmNiIi8+PHJlY3QgeD0iNiIgeT0iMTAiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAwMDAiLz48cmVjdCB4PSI1IiB5PSIxMSIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzAwMDAwMCIvPjwvc3ZnPg==');
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
