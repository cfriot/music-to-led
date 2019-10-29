const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')


/*************************************************************
 * py process
 *************************************************************/
//
// const PY_DIST_FOLDER = 'pycalcdist'
// const PY_FOLDER = 'pycalc'
// const PY_MODULE = 'api' // without .py suffix
//
// let pyProc = null
//
// const guessPackaged = () => {
//   const fullPath = path.join(__dirname, PY_DIST_FOLDER)
//   return require('fs').existsSync(fullPath)
// }
//
// const getScriptPath = () => {
//   if (!guessPackaged()) {
//     return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
//   }
//   return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
// }
//
// const createPyProc = () => {
//   let script = getScriptPath()
//
//   if (guessPackaged()) {
//     pyProc = require('child_process').execFile(script)
//   } else {
//     pyProc = require('child_process').spawn('python', [script])
//   }
//
//   if (pyProc != null) {
//     console.log('child process success')
//   }
// }
//
// const exitPyProc = () => {
//   pyProc.kill()
//   pyProc = null
// }

// app.on('ready', createPyProc)
// app.on('will-quit', exitPyProc)


/*************************************************************
 * window management
 *************************************************************/

let mainWindow = null

const createWindow = () => {

  mainWindow = new BrowserWindow({
    width: 900,
    height: 600,
    minWidth: 900,
    minHeight: 600,
    maxWidth: 1100,
    maxHeight: 800,
    center: true,
    titleBarStyle: "hidden",
    frame: false,
    titlebarAppearsTransparent: true,
    backgroundColor: "#061B28"
  })

  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'src/index.html'),
    protocol: 'file:',
    slashes: true
  }))

  mainWindow.webContents.openDevTools()

  mainWindow.on('closed', () => {
    mainWindow = null
  })

}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})
