plugins {
    id("com.android.library") version "8.2"
    kotlin("multiplatform") version "1.9.0"
    kotlin("plugin.serialization") version "1.9.0"
    id("org.jlleitschuh.gradle.ktlint") version "11.5.0"
    id("org.jetbrains.dokka") version "1.8.20"
    id("convention.publication")
}

group = "io.polywrap.plugins"
version = "0.10.4"

repositories {
    google()
    mavenCentral()
    maven { url = uri("https://s01.oss.sonatype.org/content/repositories/snapshots/") }
}

kotlin {
    jvm {
        jvmToolchain(17)
        testRuns["test"].executionTask.configure {
            useJUnitPlatform()
        }
    }
    androidTarget {
        publishLibraryVariants("release")
    }
    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("io.polywrap:polywrap-client:0.10.4")
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-core:1.5.1")
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
                implementation("io.ktor:ktor-client-core:2.3.2")
                implementation("io.ktor:ktor-client-android:2.3.2")
            }
        }
        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
                implementation("io.ktor:ktor-client-mock:2.3.2")
            }
        }
    }
}

android {
    namespace = "io.polywrap.plugins.http"
    compileSdk = 32
    defaultConfig.minSdk = 24
    compileOptions {
        targetCompatibility = JavaVersion.VERSION_17
    }
    testOptions {
        unitTests.all {
            it.enabled = false
        }
    }
}

// javadoc generation for Maven repository publication
tasks.register<Jar>("dokkaJavadocJar") {
    dependsOn(tasks.dokkaJavadoc)
    from(tasks.dokkaJavadoc.flatMap { it.outputDirectory })
    archiveClassifier.set("javadoc")
}

// print stdout during tests
tasks.withType<Test> {
    this.testLogging {
        this.showStandardStreams = true
    }
}

// lint configuration
configure<org.jlleitschuh.gradle.ktlint.KtlintExtension> {
    disabledRules.set(setOf("no-wildcard-imports"))
    filter {
        exclude("**/build/**")
        exclude("**/generated/**")
        exclude("**/resources/**")
        exclude("**/wrap/**")
        exclude("**/build.gradle.kts")
    }
}
