package main

import (
	"os"
	"testing"
)

func TestGenerateJobManifestFile(t *testing.T) {
	// Define the test case
	job := JobManifest{
		Name:      "client-monitor-job",
		Namespace: "dev",
		Action:    "dump",
		PodName:   "test-namespace-deploy-764965b55f-79l9g",
		PID:       "1",
		UID:       "NO_UID",
		NameOverride: "NO_NAME",
		Duration:  "NO_DURATION",
		Egress:    "NO_EGRESS_PROVIDER",
		Tags:      "NO_TAG",
	}

	filePath := "test-job.yml"

	// Call the function being tested
	err := generateJobManifestFile(job, filePath)
	defer os.Remove(filePath) // Clean up the created file after the test

	// Check the test result
	if err != nil {
		t.Errorf("generateJobManifestFile returned an error: %s", err)
	}

	// You can add more assertions here to verify the contents or properties of the generated file
}

func TestMain(m *testing.M) {
	// Set up any test environment or configurations

	// Run the tests
	exitCode := m.Run()

	// Clean up any resources after all tests are finished

	// Exit with the proper exit code
	os.Exit(exitCode)
}
