import {ApolloProvider} from "@apollo/client";
import client from "./lib/apolloClient.tsx";
import {CalendarPage} from "./pages/calendar/Calendar.tsx";

function App() {
  return (
    <ApolloProvider client={client}>
      <CalendarPage />
    </ApolloProvider>
  );
}

export default App;
