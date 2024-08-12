import { Hono } from 'hono'
import {cors} from 'hono/cors'


type Bindings = {

  DB:D1Database;
}

const app: Hono<{Bindings:Bindings}> = new Hono();

app.use(
  '/*',
  cors(
    {
      origin: 'http://localhot:5173',
      allowMethods: ['POST','GET','OPTIONS','DELETE']
    }
  )

)


app.get('/', (c) => {
  return c.text('Hello Hono!')
})

export default app
