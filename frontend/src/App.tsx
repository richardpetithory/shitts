import client from "@/lib/apolloClient.tsx";
import {CalendarPage} from "@/pages/calendar/Calendar.tsx";
import {ApolloProvider} from "@apollo/client";
import {Container} from "react-bootstrap";
import {Helmet, HelmetProvider} from "react-helmet-async";

function App() {
  return (
    <ApolloProvider client={client}>
      <Container>
        <HelmetProvider>
          <Helmet defaultTitle="Shitts" titleTemplate="%s | Shitts" />
          <CalendarPage />
        </HelmetProvider>
      </Container>
    </ApolloProvider>
  );
}

export default App;
