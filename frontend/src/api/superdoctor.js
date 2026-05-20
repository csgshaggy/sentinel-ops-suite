import axios from "axios";

/**
 * Call the SuperDoctor backend endpoint.
 * Returns:
 *  {
 *    summary: { ... },
 *    timings_ms: { plugin: ms },
 *    results: { plugin: [CheckResult, ...] }
 *  }
 */
export async function runSuperDoctor(mode = "LOCAL") {
  try {
    const response = await axios.get(`/admin/superdoctor/run`, {
      params: { mode },
    });
    return response.data;
  } catch (err) {
    console.error("SuperDoctor API error:", err);
    throw err;
  }
}
