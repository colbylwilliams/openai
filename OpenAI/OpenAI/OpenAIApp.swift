//
//  OpenAIApp.swift
//  OpenAI
//
//  Created by Colby L Williams on 1/24/23.
//

import SwiftUI

@main
struct OpenAIApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(ChatService())
        }
    }
}
