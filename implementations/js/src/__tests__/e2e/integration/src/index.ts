import {
  HTTP_Module,
  HTTP_Response,
  Args_get,
  Args_post,
  ModuleBase
} from "./wrap";

export class Module extends ModuleBase {
  get(args: Args_get): HTTP_Response | null {
    return HTTP_Module.get({
      url: args.url,
      request: args.request
    }).unwrap();
  }

  post(args: Args_post): HTTP_Response | null {
    return HTTP_Module.post({
      url: args.url,
      request: args.request
    }).unwrap();
  }
}
