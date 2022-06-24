import Head from 'next/head';
import { Box, Container } from '@mui/material';
import { useRouter } from "next/router";
// import { Notebook } from "../components/notebook/Notebook";
// import { NotebookProvider } from "../components/notebook/NotebookProvider";
import { Layout } from '../../components/layout/layout';


const NotebookPage = () => {
  const router = useRouter()
  const { rid } = router.query
  console.log(rid)

  return (
    <>
      <Head>
        <title>
          BOLD Profiler
        </title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8
        }}
      >
        <Container maxWidth={'lg'}>
          {/*<NotebookProvider notebookId={'878b2ca8-2b97-4a20-abd6-06903415a673'}>*/}
          {/*  <Notebook/>*/}
          {/*</NotebookProvider>*/}
        </Container>
      </Box>
    </>
  );
}

NotebookPage.getLayout = (page) => (
  <Layout showNavbar={false}>
    {page}
  </Layout>
);

export default NotebookPage;