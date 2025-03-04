import { Route, Router, Routes } from "react-router-dom"
import HomePage from "./pages/home/HomePage"
import MainLayout from "./layout/MainLayout"
import ChatPage from "./pages/chat/ChatPage"


function App() {

  return (
   <>
     <Routes>
      <Route path="/" element={<MainLayout/>}>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/chat" element={<ChatPage/>}/>
      </Route>      
     </Routes>

   </>
   
  )
}

export default App
