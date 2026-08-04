import apiRequest from "./api";

const securityService = {
  getPolicy() {
    return apiRequest("/security/policy");
  },
};

export default securityService;
