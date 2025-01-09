// App.jsx
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faClock, faMicrophone } from "@fortawesome/free-solid-svg-icons";
import styled, { keyframes } from "styled-components";

// Анимация "пульса"
const pulse = keyframes`
  0% {
    box-shadow: 0 0 0 0 rgba(25, 195, 125, 0.5);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(25, 195, 125, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(25, 195, 125, 0);
  }
`;

// Кнопка записи 
const RecordButton = styled.button`
  width: 60px;
  height: 60px;
  background-color: #19c37d; /* Слегка бирюзовый цвет */
  border: none;
  border-radius: 50%;
  cursor: pointer;
  outline: none;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: ${pulse} 2s infinite;

  /* Эффект при наведении */
  &:hover {
    filter: brightness(110%);
  }

  /* Эффект при нажатии */
  &:active {
    transform: scale(0.95);
  }
`;

// Иконка расписания (небольшая, слева сверху)
const ScheduleIcon = styled(FontAwesomeIcon)`
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 24px;
  color: #888;
`;

// Контейнер всего приложения
const AppContainer = styled.div`
  background: #fff;  /* белый фон */
  width: 100vw;
  height: 100vh;
  position: relative; /* чтобы ScheduleIcon мог позиционироваться абсолютно */
  display: flex;
  align-items: center; 
  justify-content: center;
`;

function App() {
  const handleRecordClick = () => {
    console.log("Запись начата");
  };

  return (
    <AppContainer>
      <ScheduleIcon icon={faClock} />
      <RecordButton onClick={handleRecordClick}>
        <FontAwesomeIcon icon={faMicrophone} />
      </RecordButton>
    </AppContainer>
  );
}

export default App;
